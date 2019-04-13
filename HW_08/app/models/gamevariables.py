from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base = get_base()

class GameVariables(base):
    """ Game variables table definition to reflect on database.
    """
    __tablename__ = 'gamevariables'
    AWAY_TEAM = Column(String(3), nullable=False)
    HOME_TEAM = Column(String(3), nullable=False) 
    WEEK = Column(String(4), nullable=False)
    SLOT = Column(Integer, nullable=False)
    NETWORK = Column(String(3), nullable=False)
    QUAL_POINTS = Column(Float, nullable=False)
    ROW_ID = Column(Integer, primary_key=True)
