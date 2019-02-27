from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class ShopDemand(base):
    __tablename__ = 'shopdemand'
    STOREID = Column(BigInteger, nullable=False) # Store label.
    AVG_DAILY_DEMAND= Column(Integer, nullable=False) # Doughs. (units)
    CENTERID = Column(String, primary_key=False) # Center label.
    id_ = Column(BigInteger, primary_key=True)
