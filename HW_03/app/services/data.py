from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.db.context import DBSession
from sqlalchemy.orm import aliased
from sqlalchemy import func
from app.models.centers import Centers
from app.models.goodstores import GoodStores
from app.models.shopdemand import ShopDemand
from app.services.computational.haver_vincenty import haversine_

class DataService(object):
    def __init__(self, systemname, dbfile):
        self.dbfile = dbfile
        self.systemname = systemname

    def get_cost(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
             cost = session.query(Centers.CENTER_ID, Centers.DIST_COST)
             return {obj[0] : obj[1] for obj in cost}
                 
    def get_capacity(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            capacity = session.query(Centers.CENTER_ID, Centers.SUPPLY_CAPACITY)
            return {obj[0]: int(obj[1].replace(',','')) for obj in capacity}

    def get_demand(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            demand = session.query(ShopDemand.STORE_NUMBER, func.sum(ShopDemand.PIZZA_SALES)).group_by(ShopDemand.STORE_NUMBER).all()
            return {obj[0]: obj[1] for obj in demand}

    def get_good_stores(self) -> list:
        with DBSession(self.systemname, self.dbfile) as session:
            return [obj[0] for obj in session.query(GoodStores.STORE_NUMBER)]

    def get_distances(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            distance = dict()
            data = session.execute("select a.CENTER_ID, b.STORE_NUMBER, a.LATITUDE, a.LONGITUDE, b.LATITUDE, b.LONGITUDE from centers a cross join goodstores b;")
            for center, store, center_lat, center_lon, store_lat, store_lon in data:
                 distance[center, store] = haversine_((center_lat, center_lon), (store_lat, store_lon))
            return distance
        
