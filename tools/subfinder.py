import asyncio
import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO)

async def run_subfinder(target: str, silent: bool = True, output_to_file: bool = True) -> None:
    """
    Асинхронная функция для запуска subfinder

    :param target: домен, для которого будет выполняться поиск
    :type target: str
    :param silent: флаг, означающий, что не будет вывода в stdout
    :type silent: bool
    :param output_to_file: флаг, означающий, что результаты будут сохранены в файл
    :type output_to_file: bool
    """
    try:
        command = ["subfinder", "-d", target]
        if silent:
            command.append("-silent")
        
        logging.info(f"Запуск subfinder для {target}")
        result = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = await result.communicate()
        
        stdout_str = stdout.decode()
        stderr_str = stderr.decode()

        if result.returncode == 0:
            subdomains = stdout_str.splitlines()
            logging.info(f"Найденные поддомены для {target}:")
            for subdomain in subdomains:
                logging.info(subdomain)
            
            if output_to_file:
                file_name = f"{target}_subdomains_{os.urandom(4).hex()}.txt"
                with open(file_name, "w") as f:
                    f.write("\n".join(subdomains))
                logging.info(f"Результаты сохранены в {file_name}")
        else:
            logging.error(f"Ошибка при запуске Subfinder: {stderr_str}")
    except FileNotFoundError:
        logging.error("Команда subfinder не найдена. Убедитесь, что она установлена и доступна в PATH.")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

def run_subfinder_sync(target: str, silent: bool = True, output_to_file: bool = True) -> None:
    """
    Функция для запуска асинхронной задачи find_subdomain
    """
    if not target:
        logging.error("Домен не может быть пустым")
        return
    
    asyncio.run(run_subfinder(target, silent, output_to_file))