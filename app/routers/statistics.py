from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.database import get_db
from app.models.statistics_models import Statistics
from app.schemas import Statistics as StatisticsSchema


router = APIRouter()


@router.get("/statistics", response_model=StatisticsSchema)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Statistics))
    statistics = result.scalars().first()
    if not statistics:
        return {"total_transactions": 0, "average_transaction_amount": 0.0, "top_transactions": []}

    return {
        "total_transactions": statistics.total_transactions,
        "average_transaction_amount": statistics.average_transaction_amount,
        "top_transactions": eval(statistics.top_transactions),
    }
