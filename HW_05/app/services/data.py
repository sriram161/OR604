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

    def get_mill_flour_prouction_cost(self) -> dict: # Cost of trasport from mill to center.
        with DBSession(self.systemname, self.dbfile) as session:
             cost = session.query(Mills.MILLID, Mills.PROD_COST)
             return {obj[0].replace(' ','') : obj[1] for obj in cost}
                 
    def get_center_transport_cost(self) -> dict: # Cost of trasport from mill to center.
        with DBSession(self.systemname, self.dbfile) as session:
             cost = session.query(Centers.CENTERID, Centers.DIST_COST)
             return {obj[0].replace(' ','') : obj[1] for obj in cost}
                 
    def get_demand_center(self) -> dict:  # centers capacity to meet weekly average of shop.
        with DBSession(self.systemname, self.dbfile) as session:
            demand = session.query(ShopDemand.CENTERID, func.sum(ShopDemand.AVG_DAILY_DEMAND)).group_by(ShopDemand.CENTERID).all()
            return {obj[0]: obj[1]*7 for obj in demand}

    def get_mill_capacity(self) -> dict: # Mill capacity to generate flour sack.
        with DBSession(self.systemname, self.dbfile) as session:
            capacity = session.query(Mills.MILLID, Mills.SUPPLY_CAPACITY)
            return {obj[0].replace(' ', ''): int(obj[1].replace(',', '')) for obj in capacity}

    def get_distances(self) -> dict: # Get distances matrix of mills and distribution centers.
        with DBSession(self.systemname, self.dbfile) as session:
            distance = dict()
            data = session.execute("select a.CENTERID, b.MILLID, a.LATITUDE, a.LONGITUDE, b.LATITUDE, b.LONGITUDE from centers a cross join mills b;")
            for center, mill, center_lat, center_lon, mill_lat, mill_lon in data:
                 distance[mill.replace(' ', ''), center.replace(' ', '')] = haversine_((center_lat, center_lon), (mill_lat, mill_lon))
            return distance

    def add_records(self, objects:list) -> None:
        with DBSession(self.systemname, self.dbfile) as session:
             session.add_all(objects)
    
    def get_center_capacity(self) -> dict: #TODO: need to ask prof.
        with DBSession(self.systemname, self.dbfile) as session:
            capacity = session.query(Centers.CENTERID, Centers.SUPPLY_CAPACITY)
            return {obj[0]: obj[1] for obj in capacity}
