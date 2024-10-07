import asyncio
import subprocess
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_maryam(targets: str, output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска OWASP Maryam.

    :param targets: файл с доменами или один домен для проверки.
    :type targets: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл.
    :type output_to_file: bool
    """
    try:
        # Если targets это файл, читаем домены из файла, иначе используем как один домен
        if os.path.isfile(targets):
            with open(targets, "r") as file:
                domain_list = file.read().splitlines()
        else:
            domain_list = [targets]

        for domain in domain_list:
            command = ["maryam", "-e", "info", "-d", domain]  # Команда для запуска OWASP Maryam

            logging.info(f"Запуск Maryam для домена: {domain}")
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
                logging.info(f"Результаты Maryam для {domain}:")
                logging.info(stdout_str)

                if output_to_file:
                    file_name = f"maryam_results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(file_name, "w") as f:
                        f.write(stdout_str)
                    logging.info(f"Результаты сохранены в {file_name}")
            else:
                logging.error(f"Ошибка при запуске Maryam для {domain}: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда Maryam не найдена. Убедитесь, что она установлена и доступна в PATH.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_maryam_sync(targets: str, output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_maryam синхронно
    """
    if not targets:
        logging.error("Файл с доменами или домен не может быть пустым")
        return

    asyncio.run(run_maryam(targets, output_to_file))

