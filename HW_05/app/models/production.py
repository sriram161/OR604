from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.db.settings import get_base

base=get_base()

# TODO: Check the units of data.
class Production(base):
    __tablename__ = 'production'
    CALVIN_MONTH = Column(String,  primary_key=True)
    M_1 = Column(String, nullable=False)  # gal
    M_2 = Column(String, nullable=False)  # gal
    M_3= Column(String, nullable=False) # gal
    M_4= Column(String, nullable=False) # gal
    M_5= Column(String, nullable=False) # gal
    M_6= Column(String, nullable=False) # gal
    M_7= Column(String, nullable=False) # gal
    M_8= Column(String, nullable=False) # gal
    M_9= Column(String, nullable=False) # gal
    M_10= Column(String, nullable=False) # gal
    M_11= Column(String, nullable=False) # gal
    M_12= Column(String, nullable=False) # gal
