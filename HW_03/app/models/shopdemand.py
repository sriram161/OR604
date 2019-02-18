from sqlalchemy import Column, String, BigInteger, Integer, Sequence
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class ShopDemand(base):
    __tablename__ = 'shopdemand'
    DATE = Column(String, primary_key=False)
    STORE_NUMBER = Column(BigInteger, nullable=False)
    PIZZA_SALES= Column(Integer, nullable=False)
    id_ = Column(BigInteger, primary_key=True)
    
