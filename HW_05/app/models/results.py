from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Optcows(base):
    __tablename__ = 'optcows'
    ID_ = Column(BigInteger, primary_key=True)
    CALVINMONTH = Column(String(50), nullable=False)
    COWCOUNT = Column(String(50), nullable=False)

class Optmilk(base):
    __tablename__ = 'optmilk'
    ID_ = Column(BigInteger, primary_key=True)
    DEMANDMONTH = Column(String(50), nullable=False)
    MILK = Column(String(50), nullable=False)
    FLAG =  Column(String(50), nullable=False)
