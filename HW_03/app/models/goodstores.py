from sqlalchemy import Column, String, DateTime, BigInteger,Integer, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class GoodStores(base):
    __tablename__ = 'goodstores'
    STORE_NUMBER = Column(BigInteger, primary_key=True)
    STORE = Column(BigInteger, primary_key=True)
    STREET = Column(String, nullable=False)
    CITY= Column(String, nullable=False)
    STATE= Column(String(8), nullable=False)
    ZIP= Column(Integer, nullable=False)
    LATITUDE = Column(Float, nullable=False)
    LONGITUDE = Column(Float, nullable=False)
