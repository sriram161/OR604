from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Centers(base):
    __tablename__ = 'centers'
    CENTER_ID = Column(String (50), primary_key=True)
    ADDRESS= Column(String(50), nullable=False)
    LATITUDE= Column(Float, nullable=False)
    LONGITUDE= Column(Float, nullable=False)
    SUPPLY_CAPACITY= Column(Integer, nullable=False)
    DIST_COST= Column(Float, nullable=False)
