from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

# TODO: define columns on results table.
class Schedule(base):
    __tablename__ = 'schedule'
    ROW_ID = Column(Integer, primary_key=True)