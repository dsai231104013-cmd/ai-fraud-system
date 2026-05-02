from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FraudLog(Base):
    __tablename__ = "fraud_logs"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    result = Column(String)