from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class TeamData(base):
    __tablename__ = 'teamdata'
    TEAM = Column(String(3),  nullable=False)
    CONF = Column(String(3),  nullable=False)
    DIV = Column(String(5),  nullable=False)
    QUALITY = Column(Integer,  nullable=False)
    TIMEZONE = Column(Integer,  nullable=False)
    ROW_ID = Column(Integer, primary_key=True)

