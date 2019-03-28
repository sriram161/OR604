from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class Opponents(base):
    __tablename__ = 'opponents'
    AWAY_TEAM = Column(String(3),  nullable=False)
    HOME_TEAM = Column(String(3),  nullable=False)
    ROW_ID = Column(Integer, primary_key=True)

