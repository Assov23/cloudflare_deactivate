import asyncio
import subprocess
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_catphish(domain: str, output_dir: str = "catphish_results", output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска Catphish.

    :param domain: домен для проверки через Catphish.
    :type domain: str
    :param output_dir: директория для сохранения результатов.
    :type output_dir: str
    :param output_to_file: флаг, показывающий, будут ли результаты сохранены в файл.
    :type output_to_file: bool
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        # Команда для запуска Catphish
        command = ["ruby", "./catphish/catphish.rb", domain]

        logging.info(f"Запуск Catphish для домена: {domain}")
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # Преобразуем байты в строки
        stdout_str = stdout.decode()
        stderr_str = stderr.decode()

        if process.returncode == 0:
            logging.info(f"Результаты Catphish для {domain}:")
            logging.info(stdout_str)

            if output_to_file:
                file_name = f"{output_dir}/catphish_results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(file_name, "w") as f:
                    f.write(stdout_str)
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске Catphish для {domain}: {stderr_str}")
    except FileNotFoundError:
        logging.error("Catphish не найден. Убедитесь, что catphish.rb находится в рабочей директории и Ruby установлен.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_catphish_sync(domain: str, output_dir: str = "catphish_results", output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_catphish в синхронном режиме.
    """
    if not domain:
        logging.error("Домен не может быть пустым")
        return

    asyncio.run(run_catphish(domain, output_dir, output_to_file))