import json
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def save_report_to_file(filename="report.json"):
    """
    Декоратор для сохранения результата работы функции в файл.
    Если имя файла не указано, используется имя по умолчанию.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logging.info(f"Отчет сохранен в файл: {filename}")
            return result

        return wrapper

    return decorator


@save_report_to_file()
def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> dict:
    """
    Функция для расчета средних трат в рабочий и выходной день за последние
    три месяца от заданной даты (или текущей даты).
    """
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    start_date = date - timedelta(days=90)
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    logging.info(f"Отфильтрованные транзакции: {filtered_transactions}")

    filtered_transactions["Дата операции"] = pd.to_datetime(
        filtered_transactions["Дата операции"], errors="coerce"
    )

    filtered_transactions = filtered_transactions.dropna(
        subset=["Дата операции"]
    )

    filtered_transactions["День недели"] = filtered_transactions
    ["Дата операции"].dt.day_name()

    workdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekends = ["Saturday", "Sunday"]

    average_spending = {
        "рабочие дни": filtered_transactions[
            filtered_transactions["День недели"].isin(workdays)
        ]["Сумма операции"].mean()
        or 0,
        "выходные дни": filtered_transactions[
            filtered_transactions["День недели"].isin(weekends)
        ]["Сумма операции"].mean()
        or 0,
    }

    logging.info("Средние траты по дням рассчитаны.")
    return average_spending


def load_transactions_from_excel(filepath: str) -> pd.DataFrame:
    """
    Функция для загрузки данных из Excel файла.
    """
    try:
        df = pd.read_excel(filepath)
        logging.info(f"Загруженные столбцы: {df.columns.tolist()}")

        df["Дата операции"] = pd.to_datetime(
            df["Дата операции"], errors="coerce"
        )
        df.dropna(subset=["Дата операции"], inplace=True)
        return df
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных из файла: {e}")
        return pd.DataFrame()
