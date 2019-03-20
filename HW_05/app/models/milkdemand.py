from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class MilkDemand(base):
    __tablename__ = 'milkdemand'
    MONTH = Column(Integer, primary_key=True)
    DEMAND= Column(Float, nullable=False) # gal
    PRICE= Column(Float, nullable=False) # $/gal
