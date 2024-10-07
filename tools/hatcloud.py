import asyncio
import subprocess
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_hatcloud(targets: str, output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска HatCloud.

    :param targets: файл с доменами или один домен для проверки.
    :type targets: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл.
    :type output_to_file: bool
    """
    try:
        # HatCloud принимает один домен, так что читаем из файла, если targets — файл
        if os.path.isfile(targets):
            with open(targets, "r") as file:
                domain_list = file.read().splitlines()
        else:
            domain_list = [targets]

        for domain in domain_list:
            command = ["ruby", "hatcloud.rb", domain]  # Команда для запуска HatCloud

            logging.info(f"Запуск HatCloud для {domain}")
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            # Преобразуем байтовые данные в строки
            stdout_str = stdout.decode()
            stderr_str = stderr.decode()

            if process.returncode == 0:
                logging.info(f"Результаты HatCloud для {domain}:")
                logging.info(stdout_str)

                if output_to_file:
                    file_name = f"hatcloud_results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(file_name, "w") as f:
                        f.write(stdout_str)
                    logging.info(f"Результаты сохранены в {file_name}")
            else:
                logging.error(f"Ошибка при запуске HatCloud для {domain}: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда HatCloud не найдена. Убедитесь, что Ruby установлен, и hatcloud.rb находится в рабочей директории.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_hatcloud_sync(targets: str, output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_hatcloud синхронно
    """
    if not targets:
        logging.error("Файл с доменами или домен не может быть пустым")
        return

    asyncio.run(run_hatcloud(targets, output_to_file))

