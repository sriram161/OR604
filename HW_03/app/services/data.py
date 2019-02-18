from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.db.context import DBSession
from sqlalchemy.orm import aliased
from app.models.centers import Centers
from app.models.goodstores import GoodStores
from app.models.shopdemand import ShopDemand
from app.services.computational.haver_vincenty import haversine_ as hv

class DataService(object):
    def __init__(self, systemname, dbfile):
        self.dbfile = dbfile
        self.systemname = systemname

    def get_distances(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            session.query(Centers)
    
    def get_cost(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
             session.query(Centers)

    def get_capacity(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
        pass

    def get_demand(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
        pass
    

    
