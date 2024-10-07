import asyncio
import subprocess
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_sudomy(domain: str, output_dir: str = "sudomy_results", output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска Sudomy.

    :param domain: домен для поиска поддоменов.
    :type domain: str
    :param output_dir: директория для сохранения результатов.
    :type output_dir: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл.
    :type output_to_file: bool
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        command = ["python3", "sudomy.py", "-d", domain, "-o", output_dir]  # Команда для запуска Sudomy

        logging.info(f"Запуск Sudomy для домена: {domain}")
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
            logging.info(f"Результаты Sudomy для {domain}:")
            logging.info(stdout_str)

            if output_to_file:
                file_name = f"{output_dir}/sudomy_results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(file_name, "w") as f:
                    f.write(stdout_str)
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске Sudomy для {domain}: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда Sudomy не найдена. Убедитесь, что sudomy.py находится в рабочей директории.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_sudomy_sync(domain: str, output_dir: str = "sudomy_results", output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_sudomy синхронно
    """
    if not domain:
        logging.error("Домен не может быть пустым")
        return

    asyncio.run(run_sudomy(domain, output_dir, output_to_file))

