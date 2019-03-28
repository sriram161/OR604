import csv
import codecs
from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.models.gamevariables import GameVariables
from app.models.networkslots import NetworkSlots
from app.models.opponents import Opponents
from app.models.teamdata import TeamData
from app.models.results import Schedule
from app.db.context import DBSession
from itertools import count

def create_tables(systemname, dbfile):
    base = get_base()
    sqlite_engine = DbFactory.get_db_engine(systemname, 
                                        dbfile).get_database()
    GameVariables.__table__.create(sqlite_engine, checkfirst=True)
    NetworkSlots.__table__.create(sqlite_engine, checkfirst=True)
    TeamData.__table__.create(sqlite_engine, checkfirst=True)
    Schedule.__table__.create(sqlite_engine, checkfirst=True)
    Opponents.__table__.create(sqlite_engine, checkfirst=True)
    sqlite_engine.dispose()


# TODO: code data to load in to database
def load_game_variables_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=GameVariables.metadata.tables['gamevariables'].columns.keys())
        for item in reader:
            session.add(GameVariables(**item))
        print(f"File_loaded...! {_file}")


def load_network_slot_week_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=NetworkSlots.metadata.tables['networkslots'].columns.keys())
        for item in reader:
            item['MONTH'] = int(item['MONTH'])
            item['DEMAND'] = float(item['DEMAND'])
            item['PRICE'] = float(item['PRICE'].strip(' ').strip('$'))
            session.add(MilkDemand(**item))
        print(f"File_loaded...! {_file}")


def load_opponents_table(data_path, _file, systemname, dbfile):
    with DBSession(systemname, dbfile) as session, codecs.open(data_path + _file, 'r',
                                                               encoding='ascii', errors='ignore') as f_handle:
        next(f_handle) # Skip headers of csv file.
        reader = csv.DictReader(f_handle, fieldnames=Opponents.metadata.tables['opponents'].columns.keys())
        for item in reader:
            item['CALVIN_MONTH'] = int(item['CALVIN_MONTH'].strip())
            item['FEED_COST'] = float(item['FEED_COST'].strip(' ').strip('$'))
            obj = CowFeed(**item)
            session.add(obj)
        print(f"File_loaded...! {_file}")
    

def load_team_data_table(data_path, _file, systemname, dbfile):
    pass
