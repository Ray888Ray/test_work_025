from celery import Celery
from celery import Task
import asyncio
from sqlalchemy.future import select
from app.database.database import SessionLocal
from app.models.transactions_models import Transaction
from app.models.statistics_models import Statistics
import heapq
import os
from dotenv import load_dotenv


load_dotenv()

BROKER_URL = os.getenv("BROKER")
celery = Celery("tasks", broker=BROKER_URL)


class AsyncTask(Task):
    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run(*args, **kwargs))


@celery.task(base=AsyncTask, name="tasks.update_statistics")
async def update_statistics():
    async with SessionLocal() as db:
        result = await db.execute(select(Transaction))
        transactions = result.scalars().all()

        total_transactions = len(transactions)
        total_amount = sum(tx.amount for tx in transactions)
        average_amount = total_amount / total_transactions if total_transactions > 0 else 0
        top_transactions = heapq.nlargest(3, transactions, key=lambda x: x.amount)
        top_transactions_data = [
            {"transaction_id": tx.transaction_id, "amount": tx.amount} for tx in top_transactions
        ]

        result = await db.execute(select(Statistics))
        statistics = result.scalars().first()
        if not statistics:
            statistics = Statistics(
                total_transactions=total_transactions,
                average_transaction_amount=average_amount,
                top_transactions=str(top_transactions_data),
            )
            db.add(statistics)
        else:
            statistics.total_transactions = total_transactions
            statistics.average_transaction_amount = average_amount
            statistics.top_transactions = str(top_transactions_data)

        await db.commit()
