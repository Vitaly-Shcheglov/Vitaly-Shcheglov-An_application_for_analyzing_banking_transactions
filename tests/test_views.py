import json

import pandas as pd
import pytest

from src.views import events_page


@pytest.fixture
def temp_file(tmp_path):
    """
    Создает временный файл для использования в тестах.
    """
    file_path = tmp_path / "transactions.json"
    yield file_path


def test_events_page_valid_data():
    """
    Тестирует функцию events_page с корректными данными.
    Проверяет, что функция правильно считает общее количество событий и
    количество событий по категориям.
    """
    data = pd.DataFrame(
        [
            {"Категория": "Еда", "Сумма": 150},
            {"Категория": "Еда", "Сумма": 200},
            {"Категория": "Развлечения", "Сумма": 300},
        ]
    )
    result = events_page(data)
    result_data = json.loads(result)
    assert result_data["total_events"] == 3
    assert result_data["categories"] == {"Еда": 2, "Развлечения": 1}


def test_events_page_empty_dataframe():
    """
    Тестирует функцию events_page с пустым DataFrame.
    Проверяет, что функция возвращает 0 событий и пустой словарь категорий,
    когда передается пустой DataFrame.
    """
    df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма", "Тип"])
    result = events_page(df)
    result_data = json.loads(result)
    assert result_data["total_events"] == 0
    assert result_data["categories"] == {}


def test_events_page_missing_columns():
    """
    Тестирует функцию events_page с отсутствующими обязательными колонками.
    Проверяет, что функция вызывает KeyError, если в переданном DataFrame
    отсутствуют обязательные колонки.

    """
    df = pd.DataFrame({"Дата операции": ["2024-12-01"], "Сумма": [500]})
    with pytest.raises(KeyError, match="Отсутствуют обязательные колонки"):
        events_page(df)


def test_events_page_invalid_data_format():
    """
    Тестирует функцию events_page с некорректным форматом данных.
    Проверяет, что функция игнорирует некорректные значения и правильно
    считает количество событий и категорий.
    """
    data = {
        "Категория": ["Продукты", "Транспорт", "Развлечения"],
        "Сумма": ["500", "1000", "invalid_sum"],
    }
    df = pd.DataFrame(data)
    result = events_page(df)
    result_data = json.loads(result)

    assert result_data["total_events"] == 2
    assert result_data["categories"] == {"Продукты": 1, "Транспорт": 1}
