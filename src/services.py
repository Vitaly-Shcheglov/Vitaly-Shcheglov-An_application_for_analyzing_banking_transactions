import json
import logging
from typing import Any, Dict, List
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает данные транзакций из Excel файла и возвращает список.
    """
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        logging.info("Успешно считаны транзакции из файла.")
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при чтении данных из файла: {e}")
        return []


def extract_phone_numbers(transactions: List[Dict[str, Any]]) -> set:
    """
    Извлекает уникальные телефонные номера из списка транзакций.
    """
    phone_numbers = set()
    for transaction in transactions:
        if transaction.get("phone"):
            phone_numbers.add(transaction["phone"])

    logging.info(
        f"Найдено {len(phone_numbers)} уникальных телефонных номеров."
    )
    return phone_numbers


def search_transactions(file_path: str) -> str:
    """
    Основная функция для поиска номеров телефонов в транзакциях из Excel файла.
    """
    transactions = read_transactions(file_path)
    phone_numbers = extract_phone_numbers(transactions)

    result = {
        "status": "success" if phone_numbers else "no_phone_numbers_found",
        "phone_numbers": phone_numbers,
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
