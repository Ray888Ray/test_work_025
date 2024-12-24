from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    total_transactions = Column(Integer, nullable=False)
    average_transaction_amount = Column(Float, nullable=False)
    top_transactions = Column(String, nullable=False)
