import asyncio
import subprocess
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_osrframework(username: str, output_dir: str = "osrframework_results", output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска OSRFramework (например, usufy.py).

    :param username: имя пользователя для поиска информации через OSRFramework.
    :type username: str
    :param output_dir: директория для сохранения результатов.
    :type output_dir: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл.
    :type output_to_file: bool
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        command = ["python3", "./osrframework/usufy.py", username]

        logging.info(f"Запуск OSRFramework (usufy.py) для пользователя: {username}")
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
            logging.info(f"Результаты OSRFramework для {username}:")
            logging.info(stdout_str)

            if output_to_file:
                file_name = f"{output_dir}/osrframework_results_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(file_name, "w") as f:
                    f.write(stdout_str)
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске OSRFramework для {username}: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда OSRFramework не найдена. Убедитесь, что usufy.py находится в рабочей директории.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_osrframework_sync(username: str, output_dir: str = "osrframework_results", output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_osrframework синхронно.
    """
    if not username:
        logging.error("Имя пользователя не может быть пустым")
        return

    asyncio.run(run_osrframework(username, output_dir, output_to_file))