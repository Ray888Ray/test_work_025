import pytest
from app.schemas import TransactionCreate, Statistics


def test_transaction_create_schema():
    mock_data = {
        "transaction_id": "tx001",
        "user_id": "user1",
        "amount": 100.5,
        "currency": "USD",
        "timestamp": "2024-12-23T10:00:00"
    }

    transaction = TransactionCreate(**mock_data)

    assert transaction.transaction_id == mock_data["transaction_id"]
    assert transaction.amount == mock_data["amount"]
    assert transaction.timestamp.year == 2024

    invalid_data = {
        **mock_data,
        "amount": "invalid_amount",
    }

    with pytest.raises(ValueError):
        TransactionCreate(**invalid_data)


def test_statistics_schema():
    mock_data = {
        "total_transactions": 10,
        "average_transaction_amount": 150.0,
        "top_transactions": [{"transaction_id": "tx001", "amount": 200.0}]
    }

    statistics = Statistics(**mock_data)

    assert statistics.total_transactions == mock_data["total_transactions"]
    assert statistics.average_transaction_amount == mock_data["average_transaction_amount"]
    assert statistics.top_transactions[0]["transaction_id"] == mock_data["top_transactions"][0]["transaction_id"]

    invalid_data = {
        **mock_data,
        "top_transactions": "invalid_top_transactions",
    }

    with pytest.raises(ValueError):
        Statistics(**invalid_data)
