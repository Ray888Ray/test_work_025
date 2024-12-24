from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.database.database import get_db
from app.models.transactions_models import Transaction
from app.routers.api_key_auth import api_key_auth
from app.schemas import TransactionCreate
from dotenv import load_dotenv
import os
from celery import Celery
from sqlalchemy.sql import text


load_dotenv()

BROKER_URL = os.getenv("BROKER")

celery = Celery("tasks", broker=BROKER_URL)
router = APIRouter()


@router.post("/transactions", dependencies=[Depends(api_key_auth)])
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Transaction).filter_by(transaction_id=transaction.transaction_id))
        existing_transaction = result.scalars().first()


        if existing_transaction:
            raise HTTPException(status_code=400, detail="Transaction ID must be unique")

        db_transaction = Transaction(**transaction.dict())
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)

        task = celery.send_task("tasks.update_statistics")
        return {"message": "Transaction received", "task_id": task.id}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.delete("/transactions")
async def delete_transactions(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("DELETE FROM transactions"))
        await db.commit()
        return {"message": "All transactions deleted"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/transactions")
async def get_transactions(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Transaction))
        transactions = result.scalars().all()
        return transactions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.delete("/transactions/{transaction_id}")
async def delete_transaction_by_id(transaction_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalars().first()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        await db.delete(transaction)
        await db.commit()
        return {"message": f"Transaction with ID {transaction_id} has been deleted"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
