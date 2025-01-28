import json

import pandas as pd

from my_log_config import setup_logger

events_logger = setup_logger("events", "logs/events.log")


def events_page(data: pd.DataFrame) -> str:
    """
    Функция обрабатывает события из DataFrame и возвращает JSON с анализом
    категорий.
    """
    events_logger.info("Начало обработки событий.")

    required_columns = {"Категория", "Сумма"}
    if not required_columns.issubset(data.columns):
        events_logger.error(
            f"Отсутствуют обязательные колонки: {required_columns -
                                                 set(data.columns)}"
        )
        raise KeyError(
            f"Отсутствуют обязательные колонки: {required_columns -
                                                 set(data.columns)}"
        )

    data["Сумма"] = pd.to_numeric(data["Сумма"], errors="coerce")
    valid_data = data.dropna(subset=["Сумма"])

    if valid_data.empty:
        events_logger.warning("DataFrame пуст.")
        return json.dumps(
            {"total_events": 0, "categories": {}}, ensure_ascii=False, indent=4
        )

    category_counts = valid_data["Категория"].value_counts().to_dict()
    total_events = valid_data.shape[0]

    events_logger.info(f"Обработано {total_events} событий.")
    return json.dumps(
        {"total_events": total_events, "categories": category_counts},
        ensure_ascii=False,
        indent=4,
    )
