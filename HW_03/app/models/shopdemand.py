from sqlalchemy import Column, DateTime, BigInteger, Integer
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class ShopDemand(base):
    __tablename__ = 'shopdemand'
    DATE = Column(DateTime, primary_key=True)
    STORE_NUMBER = Column(BigInteger, nullable=False)
    PIZZA_SALES= Column(Integer, nullable=False)
    