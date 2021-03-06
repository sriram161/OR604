from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class NetworkSlots(base):
    __tablename__ = 'networkslots'
    WEEK = Column(String(2), nullable=False)
    SLOT = Column(String(4), nullable=False)
    NETWORK = Column(String(3), nullable=False)
    ROW_ID = Column(Integer, primary_key=True)
