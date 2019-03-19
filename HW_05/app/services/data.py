from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.db.context import DBSession
from sqlalchemy.orm import aliased
from sqlalchemy import func
from app.models.production import Production
from app.models.milkdemand import MilkDemand
from app.models.cowfeed import CowFeed 
from app.services.computational.haver_vincenty import haversine_

class DataService(object):
    def __init__(self, systemname, dbfile):
        self.dbfile = dbfile
        self.systemname = systemname

    def get_milk_production(self) -> dict:
        """ milk prodiction matrix (calving_month, demand_month)"""
        with DBSession(self.systemname, self.dbfile) as session:
            cost = session.query(Production.CALVIN_MONTH,
                                  Production.M_1,
                                  Production.M_2,
                                  Production.M_3,
                                  Production.M_4,
                                  Production.M_5,
                                  Production.M_6,
                                  Production.M_7,
                                  Production.M_8,
                                  Production.M_9,
                                  Production.M_10,
                                  Production.M_11,
                                  Production.M_12)
            return {(int(obj[0]),idx) : float(item) for obj in cost for idx, item in enumerate(obj[1:], start=1)}
                 
    def get_feed_cost(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            """ Feed cost indexed by calving month ($/cow)"""
            cost = session.query(CowFeed.CALVIN_MONTH, CowFeed.FEED_COST)
            return {obj[0]: obj[1] for obj in cost}
                 
    def get_milk_demand(self) -> dict:
        """ Milk demand indexed by demand month (gals)"""
        with DBSession(self.systemname, self.dbfile) as session:
            demand = session.query(MilkDemand.MONTH, MilkDemand.DEMAND)
            return {obj[0]: obj[1] for obj in demand}

    def get_milk_price(self) -> dict:
        """ Milk market selling price indexed by demand month ($/gal)"""
        with DBSession(self.systemname, self.dbfile) as session:
            price = session.query(MilkDemand.MONTH,MilkDemand.PRICE)
            return {obj[0]: obj[1] for obj in price}

    def add_records(self, objects:list) -> None:
        with DBSession(self.systemname, self.dbfile) as session:
             session.add_all(objects)
    
