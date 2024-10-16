import asyncio
import logging
import re
import os

from tools.subfinder import run_subfinder
from tools.cloudfail import run_cloudfail
from tools.reconbulk import run_reconbulk
from tools.hatcloud import run_hatcloud
from tools.maryam import run_maryam
from tools.cloudunflare import run_cloudunflare
from tools.bypass_firewall import run_bypass_firewall
from tools.orsframe_work import run_osrframework

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def execute_tool(choice, target):
    try:
        tools_dict = {
            1: run_subfinder,
            2: run_cloudfail,
            3: run_reconbulk,
            4: run_hatcloud,
            5: run_maryam,
            6: run_cloudunflare,
            7: run_bypass_firewall,
            8: run_osrframework
        }
        logging.info(f"Запуск {tools_dict[choice].__name__} для {target}")
        await tools_dict[choice](target, output_to_file=True)
    except Exception as e:
        logging.error(f"Ошибка при выполнении инструмента: {e}")

def is_valid_domain(domain):
    # Простейшая проверка формата домена
    
    regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}'
    return re.match(regex, domain) is not None

async def main():
    tools = {
        1: "Subfinder (поиск поддоменов)",
        2: "CloudFail (защита и проверка доменов)",
        3: "ReconBulk (массовая проверка доменов)",
        4: "HatCloud (выяснить реальный IP)",
        5: "Maryam (сбор информации по домену)",
        6: "CloudUnflare (Bash-скрипт)",
        7: "BypassFirewall (пытается найти реальный IP)",
        8: "OSRFramework (сбор информации по домену)"
    }

    while True:
        print("Выберите инструмент для работы с доменом:")
        for key, value in tools.items():
            print(f"{key}. {value}")

        try:
            choice = int(input("Введите номер инструмента (1-7): "))
            if choice not in tools:
                raise ValueError("Неверный выбор.")
        except ValueError as e:
            logging.error(e)
            continue

        target = input("Введите домен или путь к файлу с доменами: ").strip()
        if not target or (not is_valid_domain(target) and not os.path.isfile(target)):
            logging.error("Вы не ввели действительный домен или путь к файлу. Попробуйте снова.")
            continue

        await execute_tool(choice, target)

        answer = input("Хотите продолжить? (y/n): ")
        if answer.lower() != "y":
            break

if __name__ == "__main__":
    asyncio.run(main())