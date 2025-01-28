import numpy as np
import pandas as pd
import pytest

from src.reports import spending_by_workday


def spending_by_workday(transactions: pd.DataFrame) -> dict:
    """
    Рассчитывает количество уникальных рабочих дней и общую сумму расходов.
    """
    if transactions.empty:
        return {"рабочие дни": 0, "сумма расходов": 0}

    transactions = transactions.dropna()

    with pd.option_context("mode.chained_assignment", None):
        transactions["рабочий_день"] = transactions["дата"].dt.date
        рабочие_дни = transactions["рабочий_день"].nunique()
        сумма_расходов = transactions["сумма"].sum()

    return {"рабочие дни": рабочие_дни, "сумма расходов": сумма_расходов}


def test_spending_by_workday():
    """
    Тестирование функции spending_by_workday с обычными данными.
    Проверяет, что функция правильно считает количество рабочих дней
    и сумму расходов.
    """
    data = {
        "дата": pd.date_range(start="2023-01-01", periods=5, freq="B"),
        "сумма": [100, 200, 150, 300, 250],
    }
    transactions = pd.DataFrame(data)

    result = spending_by_workday(transactions)

    assert result["рабочие дни"] == 5.0
    assert result["сумма расходов"] == 1000


def test_spending_by_workday_no_transactions():
    """
    Тестирование функции spending_by_workday, когда не переданы транзакции.
    Проверяет, что функция возвращает 0 рабочих дней и сумму расходов.
    """
    transactions = pd.DataFrame(columns=["дата", "сумма"])

    result = spending_by_workday(transactions)

    assert result["рабочие дни"] == 0
    assert result["сумма расходов"] == 0


def test_spending_by_workday_with_nan():
    """
    Тестирование функции spending_by_workday с данными, содержащими NaN.
    Проверяет, что функция правильно игнорирует NaN значения и считает
    рабочие дни и сумму расходов.
    """
    data = {
        "дата": pd.date_range(start="2023-01-01", periods=5, freq="B"),
        "сумма": [100, np.nan, 150, 300, np.nan],
    }
    transactions = pd.DataFrame(data)

    result = spending_by_workday(transactions)

    assert result["рабочие дни"] == 3.0
    assert result["сумма расходов"] == 550


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """
    Создает тестовые данные для транзакций.
    """
    return pd.DataFrame(
        {
            "дата": pd.date_range(start="2023-01-01", periods=5, freq="B"),
            "сумма": [100, 200, 300, 400, 500],
        }
    )


def test_spending_by_workday_fixture(sample_transactions):
    """
    Тестирование функции spending_by_workday с использованием фикстуры.
    Проверяет, что функция правильно обрабатывает транзакции, переданные
    через фикстуру.
    """
    result = spending_by_workday(sample_transactions)

    assert result["рабочие дни"] == 5.0
    assert result["сумма расходов"] == 1500
