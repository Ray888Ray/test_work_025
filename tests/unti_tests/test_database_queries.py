from unittest.mock import AsyncMock, MagicMock
from app.models.transactions_models import Transaction
import pytest


@pytest.mark.asyncio
async def test_database_query():
    mock_transaction = Transaction(
        transaction_id="tx001",
        user_id="user1",
        amount=100.0,
        currency="USD",
        timestamp="2024-12-23T10:00:00"
    )

    async_session = AsyncMock()
    async_session.add = AsyncMock()
    async_session.commit = AsyncMock()
    async_session.execute = AsyncMock()

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_transaction
    async_session.execute.return_value = mock_result

    await async_session.add(mock_transaction)
    await async_session.commit()

    result = await async_session.execute("mocked query")
    fetched_transaction = result.scalars().first()

    assert fetched_transaction.transaction_id == "tx001"
    assert fetched_transaction.amount == 100.0

    async_session.add.assert_called_once_with(mock_transaction)
    async_session.commit.assert_called_once()
    async_session.execute.assert_called_once_with("mocked query")
