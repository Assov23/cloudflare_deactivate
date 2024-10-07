import os
import subprocess
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def run_cloudfail(target: str, output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска cloudfail
    :param target: домен, для которого будет выполняться поиск
    :type target: str
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл
    :type output_to_file: bool
    """
    try:
        command = ["cloudfail", "--target", target]
        result = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await result.communicate()
        
        stdout_str = stdout.decode()
        stderr_str = stderr.decode()

        if result.returncode == 0:
            logging.info(f"Результаты CloudFail для {target}:")
            logging.info(stdout_str)
            
            if output_to_file:
                file_name = f"{target}_cloudfail_{os.urandom(4).hex()}.txt"
                with open(file_name, "w") as f:
                    f.write(stdout_str)
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске CloudFail: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда cloudfail не найдена. Убедитесь, что она установлена и доступна в PATH.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_cloudfail_sync(target: str, output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи run_cloudfail
    """
    if not target:
        logging.error("Домен не может быть пустым")
        return

    asyncio.run(run_cloudfail(target, output_to_file))