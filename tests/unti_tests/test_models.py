from unittest.mock import MagicMock
from app.models.transactions_models import Transaction
from app.models.statistics_models import Statistics


def test_transaction_model():
    transaction = Transaction(
        transaction_id="tx001",
        user_id="user1",
        amount=100.5,
        currency="USD",
        timestamp="2024-12-23T10:00:00"
    )

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()
    mock_session.execute.return_value.scalars.return_value.first.return_value = transaction

    mock_session.add(transaction)
    mock_session.commit()
    mock_session.refresh(transaction)

    result = mock_session.execute().scalars().first()

    assert result.transaction_id == "tx001"
    assert result.amount == 100.5


def test_statistics_model():
    statistics = Statistics(
        total_transactions=10,
        average_transaction_amount=150.0,
        top_transactions='[{"transaction_id": "tx001", "amount": 200.0}]'
    )

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()
    mock_session.execute.return_value.scalars.return_value.first.return_value = statistics

    mock_session.add(statistics)
    mock_session.commit()
    mock_session.refresh(statistics)

    result = mock_session.execute().scalars().first()

    assert result.total_transactions == 10
    assert result.average_transaction_amount == 150.0
