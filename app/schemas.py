from pydantic import BaseModel, Field
from datetime import datetime


class TransactionCreate(BaseModel):
    transaction_id: str = Field(min_length=1, description="Transaction ID must not be empty")
    user_id: str = Field(min_length=1, description="User ID must not be empty")
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    currency: str = Field(min_length=1, description="Currency must not be empty")
    timestamp: datetime = Field(description="Timestamp is required")

class Statistics(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list[dict]
