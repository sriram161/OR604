import csv
import codecs
from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.models.production import Production
from app.models.cowfeed import CowFeed
from app.models.milkdemand import MilkDemand
from app.models.results import Optcows, Optmilk
from app.db.context import DBSession
from itertools import count

def create_tables(systemname, dbfile):
    base = get_base()
    sqlite_engine = DbFactory.get_db_engine(systemname, 
                                        dbfile).get_database()
    Production.__table__.create(sqlite_engine, checkfirst=True)
    MilkDemand.__table__.create(sqlite_engine, checkfirst=True)
    CowFeed.__table__.create(sqlite_engine, checkfirst=True)
    Optcows.__table__.create(sqlite_engine, checkfirst=True)
    Optmilk.__table__.create(sqlite_engine, checkfirst=True)
    sqlite_engine.dispose()

def load_production_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=Production.metadata.tables['production'].columns.keys())
        for item in reader:
            item.pop(None)
            session.add(Production(**item))
        print(f"File_loaded...! {_file}")

def load_milkdemand_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=MilkDemand.metadata.tables['milkdemand'].columns.keys())
        for item in reader:
            item['MONTH'] = int(item['MONTH'])
            item['DEMAND'] = float(item['DEMAND'])
            item['PRICE'] = float(item['PRICE'].strip(' ').strip('$'))
            session.add(MilkDemand(**item))
        print(f"File_loaded...! {_file}")


def load_cowfeed_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=CowFeed.metadata.tables['cowfeed'].columns.keys())
        for item in reader:
            item['CALVIN_MONTH'] = int(item['CALVIN_MONTH'].strip())
            item['FEED_COST'] = float(item['FEED_COST'].strip(' ').strip('$'))
            obj = CowFeed(**item)
            session.add(obj)
        print(f"File_loaded...! {_file}")
