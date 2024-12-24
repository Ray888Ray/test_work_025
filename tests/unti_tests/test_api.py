from unittest.mock import AsyncMock, ANY
from fastapi import HTTPException
from sqlalchemy import text, select
from sqlalchemy.exc import SQLAlchemyError
import pytest
from datetime import datetime
from app.models.transactions_models import Transaction
from app.routers.transactions import create_transaction
from app.schemas import TransactionCreate
from app.routers.transactions import delete_transactions, get_transactions, delete_transaction_by_id


@pytest.fixture
def test_transactions_data():
    return TransactionCreate(
        transaction_id="123",
        user_id="user_0011",
        amount=100.0,
        currency="USD",
        timestamp=datetime.now(),
    )


@pytest.mark.asyncio
async def test_create_transaction_duplicate_transaction_id(test_db, test_transactions_data):
    db_transaction = Transaction(**test_transactions_data.model_dump())
    test_db.add(db_transaction)
    await test_db.commit()

    with pytest.raises(HTTPException) as exc_info:
        await create_transaction(test_transactions_data, db=test_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Transaction ID must be unique"


@pytest.mark.asyncio
async def test_create_transaction_duplicate_transaction_id(test_db, test_transactions_data):
    try:
        db_transaction = Transaction(**test_transactions_data.model_dump())
        test_db.add(db_transaction)
        await test_db.commit()
    except Exception:
        await test_db.rollback()

    with pytest.raises(Exception) as exc_info:
        await create_transaction(test_transactions_data, db=test_db)

    assert exc_info.value.status_code == 500
    assert "Transaction ID must be unique" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_transaction_database_error(test_transactions_data):
    mock_db = AsyncMock()
    mock_db.execute.side_effect = SQLAlchemyError("Simulated DB Error")

    with pytest.raises(Exception) as exc_info:
        await create_transaction(test_transactions_data, db=mock_db)

    assert exc_info.value.status_code == 500
    assert "Database Error: Simulated DB Error" in exc_info.value.detail
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_create_transaction_internal_server_error(test_transactions_data):
    mock_db = AsyncMock()
    mock_db.execute.side_effect = Exception("Simulated General Error")

    with pytest.raises(Exception) as exc_info:
        await create_transaction(test_transactions_data, db=mock_db)

    assert exc_info.value.status_code == 500
    assert "Internal Server Error: Simulated General Error" in exc_info.value.detail
    mock_db.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_delete_transactions_success():
    mock_db = AsyncMock()
    mock_db.execute.return_value = AsyncMock()

    response = await delete_transactions(db=mock_db)

    assert response == {"message": "All transactions deleted"}
    mock_db.execute.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_transactions_database_error():
    mock_db = AsyncMock()
    mock_db.execute.side_effect = SQLAlchemyError("Simulated DB Error")

    with pytest.raises(HTTPException) as exc_info:
        await delete_transactions(db=mock_db)

    assert exc_info.value.status_code == 500
    assert "Internal Server Error: Simulated DB Error" in exc_info.value.detail
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_get_transactions_database_error():
    mock_db = AsyncMock()
    mock_db.execute.side_effect = SQLAlchemyError("Simulated DB Error")

    with pytest.raises(HTTPException) as exc_info:
        await get_transactions(db=mock_db)

    assert exc_info.value.status_code == 500
    assert "Internal Server Error: Simulated DB Error" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_transaction_by_id_database_error():
    mock_db = AsyncMock()
    mock_db.execute.side_effect = SQLAlchemyError("Simulated DB Error")

    with pytest.raises(HTTPException) as exc_info:
        await delete_transaction_by_id(transaction_id=1, db=mock_db)

    assert exc_info.value.status_code == 500
    assert "Internal Server Error: Simulated DB Error" in exc_info.value.detail
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_get_transactions(test_db):
    from uuid import uuid4

    async with test_db.begin():
        await test_db.execute(text("DELETE FROM transactions"))

    test_transactions = [
        Transaction(
            transaction_id=str(uuid4()),
            user_id="user_001",
            amount=100.0,
            currency="USD",
            timestamp=datetime.strptime("2024-12-24", "%Y-%m-%d"),
        ),
        Transaction(
            transaction_id=str(uuid4()),
            user_id="user_002",
            amount=200.0,
            currency="EUR",
            timestamp=datetime.strptime("2024-12-24", "%Y-%m-%d"),
        ),
    ]
    test_db.add_all(test_transactions)
    await test_db.commit()

    response = await get_transactions(db=test_db)

    assert len(response) == 2
    assert response[0].user_id == "user_001"
    assert response[1].user_id == "user_002"


@pytest.mark.asyncio
async def test_delete_transaction_by_id_with_fixed_id(test_db):
    async with test_db.begin():
        await test_db.execute(text("DELETE FROM transactions"))

    db_transaction = Transaction(
        id=1,
        transaction_id="123",
        user_id="user_001",
        amount=100.0,
        currency="USD",
        timestamp=datetime.strptime("2024-12-24", "%Y-%m-%d"),
    )
    test_db.add(db_transaction)
    await test_db.commit()

    response = await delete_transaction_by_id(transaction_id=1, db=test_db)

    assert response == {"message": "Transaction with ID 1 has been deleted"}
    deleted_transaction = await test_db.execute(
        select(Transaction).where(Transaction.id == 1)
    )
    assert deleted_transaction.scalars().first() is None
