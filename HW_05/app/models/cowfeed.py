from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class CowFeed(base):
    __tablename__ = 'cowfeed'
    CALVIN_MONTH = Column(Integer, primary_key=True)
    FEED_COST = Column(Float, nullable=False) # $/years
