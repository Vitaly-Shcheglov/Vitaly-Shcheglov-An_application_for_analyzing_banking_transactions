from unittest.mock import MagicMock, patch

import pytest

from src.services import extract_phone_numbers, read_transactions


@pytest.fixture
def mock_transactions():
    """
    Создает фиктивные данные транзакций для тестирования.
    """
    return [
        {"id": 1, "name": "John Doe", "phone": "+1-555-0123"},
        {"id": 2, "name": "Jane Smith", "phone": "+1(555)456-7890"},
        {"id": 3, "name": "Bob Brown", "phone": None},
        {"id": 4, "name": "Alice Green", "phone": "+44 20 1234 5678"},
        {"id": 5, "name": "Charlie Blue", "phone": "+1-555-0123"},
    ]


@patch("src.services.pd.read_excel")
def test_read_transactions(mock_read_excel):
    """
    Тестирует функцию read_transactions.
    Использует mock для имитации чтения данных из Excel файла и проверяет,
    что функция корректно возвращает ожидаемые данные.
    """
    mock_read_excel.return_value = MagicMock(
        to_dict=lambda orient: [{"id": 1, "amount": 100}]
    )

    result = read_transactions("mock_file.xlsx")

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_extract_phone_numbers(mock_transactions):
    """
    Тестирует функцию extract_phone_numbers.
    Проверяет, что функция правильно извлекает уникальные номера телефонов
    из списка транзакций.
    """
    expected_numbers = {
        "+1-555-0123",
        "+1(555)456-7890",
        "+44 20 1234 5678",
    }

    result = extract_phone_numbers(mock_transactions)

    assert set(result) == expected_numbers


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {"name": "User One", "phone": "+1-555-0123"},
                {"name": "User Two", "phone": "+1(555)456-7890"},
            ],
            {"+1-555-0123", "+1(555)456-7890"},
        ),
        (
            [
                {"name": "User One", "phone": None},
                {"name": "User Two", "phone": None},
            ],
            set(),
        ),
        (
            [
                {"name": "User One", "phone": "+1-555-0123"},
                {"name": "User Two", "phone": "+1-555-0123"},
                {"name": "User Three", "phone": "+44 20 1234 5678"},
            ],
            {"+1-555-0123", "+44 20 1234 5678"},
        ),
    ],
)


def test_extract_phone_numbers_parametrized(transactions, expected):
    """
    Параметризованный тест для функции extract_phone_numbers.
    Проверяет, что функция правильно обрабатывает различные наборы данных
    и возвращает ожидаемые уникальные номера телефонов.
    """
    result = extract_phone_numbers(transactions)

    assert set(result) == expected
