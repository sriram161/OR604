from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Results(base):
    __tablename__ = 'results'
    ID_ = Column(BigInteger, primary_key=True)
    CENTER_ID = Column(String(50), nullable=False)
    STORE_NUMBER= Column(String(50), nullable=False)
    DOUGHS_VALUE= Column(Float, nullable=False)
