from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Results(base):
    __tablename__ = 'results'
    CENTER_ID = Column(String(50), primary_key=True)
    STORE_NUMBER= Column(String(50), nullable=False)
    DOUGHS_VALUE= Column(Float, nullable=False)
