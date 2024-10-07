import asyncio
import subprocess
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

async def run_reconbulk(targets: str, output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска ReconBulk.

    :param targets: файл с доменами или один домен для проверки.
    :type targets: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл.
    :type output_to_file: bool
    """
    try:
        command = ["ReconBulk", "-f", targets]  # Опция -f предполагает использование файла с доменами

        logging.info(f"Запуск ReconBulk для {targets}")
        # Убираем параметр text=True и декодируем вывод вручную
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
            logging.info(f"Результаты ReconBulk для {targets}:")
            logging.info(stdout_str)

            if output_to_file:
                file_name = f"reconbulk_results_{os.path.basename(targets)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(file_name, "w") as f:
                    f.write(stdout_str)
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске ReconBulk: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда ReconBulk не найдена. Убедитесь, что она установлена и доступна в PATH.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_reconbulk_sync(targets: str, output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_reconbulk
    """
    if not targets:
        logging.error("Файл с доменами или домен не может быть пустым")
        return

    asyncio.run(run_reconbulk(targets, output_to_file))
