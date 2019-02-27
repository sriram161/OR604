from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Mills(base):
    __tablename__ = 'mills'
    MILLID = Column(String(50), primary_key=True)
    LATITUDE= Column(Float, nullable=False)
    LONGITUDE= Column(Float, nullable=False)
    SUPPLY_CAPACITY= Column(Integer, nullable=False) # (Uint/ week) units.
    DIST_COST= Column(Float, nullable=False) # ($/ mile) units.
