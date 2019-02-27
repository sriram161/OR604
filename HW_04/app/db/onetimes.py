import csv
import codecs
from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.models.centers import Centers
from app.models.mills import Mills
from app.models.shopdemand import ShopDemand
from app.models.results import Results
from app.db.context import DBSession
from itertools import count

def create_tables(systemname, dbfile):
    base = get_base()
    sqlite_engine = DbFactory.get_db_engine(systemname, 
                                        dbfile).get_database()
    Centers.__table__.create(sqlite_engine, checkfirst=True)
    Mills.__table__.create(sqlite_engine, checkfirst=True)
    ShopDemand.__table__.create(sqlite_engine, checkfirst=True)
    Results.__table__.create(sqlite_engine, checkfirst=True)
    sqlite_engine.dispose()

def load_centers_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=Centers.metadata.tables['centers'].columns.keys())
        for item in reader:
            session.add(Centers(**item))
        print(f"File_loaded...! {_file}")

def load_mills_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=Mills.metadata.tables['mills'].columns.keys())
        for item in reader:
            session.add(Mills(**item))
        print(f"File_loaded...! {_file}")


def load_shopdemand_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=ShopDemand.metadata.tables['shopdemand'].columns.keys())
        row_count = count(1)
        for item in reader:
            obj = ShopDemand(**item)
            obj.id_ = next(row_count)
            session.add(obj)
        print(f"File_loaded...! {_file}")
