import argparse
import logging
import os
import sys

import pandas as pd

from my_log_config import setup_logger
from src.services import search_transactions
from src.views import events_page

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s -" " %(message)s"
)
events_logger = setup_logger("events", "logs/events.log")


def main_transactions(file_path: str):
    """Основная функция для запуска процесса поиска телефонных номеров."""
    logging.info(f"Запуск поиска телефонных номеров в файле: {file_path}")
    result = search_transactions(file_path)
    print(result)


def main_events(file_path: str):
    """Основная функция для обработки событий."""
    events_logger.info(f"Запуск обработки событий из файла: {file_path}")
    try:
        data = pd.read_excel(file_path)
        events_logger.info("Данные успешно загружены из Excel файла.")
    except Exception as e:
        events_logger.error(f"Ошибка при загрузке данных из файла: {e}")
        sys.exit(1)

    try:
        result = events_page(data)
        print(result)
    except KeyError as e:
        events_logger.error(f"Ошибка: {e}")
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Обработка транзакций и событий из Excel файлов."
    )
    parser.add_argument(
        "process_type",
        choices=["transactions", "events"],
        help="Тип обработки: 'transactions' для транзакций или 'events' для событий.",
    )
    parser.add_argument("file_path", help="Путь к Excel файлу для обработки.")

    # Парсим аргументы
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print(f"Файл не найден: {args.file_path}")
        sys.exit(1)

    # Выбор функции обработки в зависимости от типа
    if args.process_type == "transactions":
        main_transactions(args.file_path)
    elif args.process_type == "events":
        main_events(args.file_path)
