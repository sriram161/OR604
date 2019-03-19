from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Results(base):
    __tablename__ = 'results'
    ID_ = Column(BigInteger, primary_key=True)
    CALVINMONTH = Column(String(50), nullable=False)
    COWCOUNT = Column(String(50), nullable=False)
    SCENARIO = Column(String(50), nullable=False)
