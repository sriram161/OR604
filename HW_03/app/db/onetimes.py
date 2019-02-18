import csv
import codecs
from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.models.centers import Centers
from app.models.goodstores import GoodStores
from app.models.shopdemand import ShopDemand
from app.db.context import DBSession
from itertools import count


def create_tables(systemname, dbfile):
    base = get_base()
    sqlite_engine = DbFactory.get_db_engine(systemname, 
                                        dbfile).get_database()
    Centers.__table__.create(sqlite_engine, checkfirst=True)
    GoodStores.__table__.create(sqlite_engine, checkfirst=True)
    ShopDemand.__table__.create(sqlite_engine, checkfirst=True)
    sqlite_engine.dispose()


def load_centers_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=Centers.metadata.tables['centers'].columns.keys())
        for item in reader:
            session.add(Centers(**item))
        print("File_loaded...! {}".format(_file))


def load_goodstores_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle)  # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=GoodStores.metadata.tables['goodstores'].columns.keys())
        for item in reader:
            session.add(GoodStores(**item))
        print("File_loaded...! {}".format(_file))


def load_shopdemand_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle)  # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=ShopDemand.metadata.tables['shopdemand'].columns.keys())
        row_count = count(1)
        for item in reader:
            obj = ShopDemand(**item)
            obj.id_ = next(row_count)
            session.add(obj)
            if obj.id_ % 100000 == 0:
                print("db session committed at", obj.id_, " row!")
                session.commit()
        print("File_loaded...! {}".format(_file))
