from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class Mills(base):
    __tablename__ = 'mills'
    MILLID = Column(String(50), primary_key=True)
    LATITUDE= Column(Float, nullable=False)
    LONGITUDE= Column(Float, nullable=False)
    SUPPLY_CAPACITY= Column(Integer, nullable=False) # (sack unit/ week)
    PROD_COST= Column(Float, nullable=False) # ($/sack unit)

# Mills distribute to Centers.
