from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

class Trip(base):
    """ Trip table model definition. Which is used as schema to reflect records on to the 
    database table.
    """
    __tablename__ = 'trip'
    ROW_ID = Column(BigInteger, primary_key=True)
    TRIP_DURATION = Column(BigInteger, nullable=False)
    START_DATE= Column(String, nullable=False)
    START_STATION= Column(String(8), nullable=False)
    STOP_DATE= Column(String, nullable=False)
    STOP_STATION= Column(String(8), nullable=False)
    BIKE_ID= Column(String(6), nullable=False)
    USER_TYPE= Column(String(15), nullable=False)
