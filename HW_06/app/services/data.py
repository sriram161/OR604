from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory
from app.db.settings import get_base
from app.db.context import DBSession
from sqlalchemy.orm import aliased
from sqlalchemy import func
from app.models.gamevariables import GameVariables
from app.models.networkslots import NetworkSlots
from app.models.opponents import Opponents
from app.models.teamdata import TeamData
from collections import defaultdict

from app.services.computational.haver_vincenty import haversine_

class DataService(object):
    def __init__(self, systemname, dbfile):
        self.dbfile = dbfile
        self.systemname = systemname

    def get_away_dict(self) -> dict:
        """ away matrix key:- team value :- list of teams"""
        with DBSession(self.systemname, self.dbfile) as session:
            away_map = defaultdict(set)
            aways = session.query(Opponents.AWAY_TEAM, Opponents.HOME_TEAM)
            for item in aways:
                away_map[item[0]].add(item[1])
            for key in away_map.keys(): # add bye opponent to all away teams.
                away_map[key].add('BYE')
            return away_map

    def get_home_dict(self) -> dict:
        with DBSession(self.systemname, self.dbfile) as session:
            home_map = defaultdict(set)
            homes = session.query(Opponents.HOME_TEAM, Opponents.AWAY_TEAM)
            for item in homes:
                home_map[item[0]].add(item[1])
            home_teams = set(home_map.keys())
            home_map['BYE'] = home_teams # Add bye home team for all teams.
            return home_map

    def get_team_list(self) -> set:
        with DBSession(self.systemname, self.dbfile) as session:
            teams = session.query(TeamData.TEAM).distinct()
            return {item[0] for item in teams}

    def get_network_list(self) -> list:
        with DBSession(self.systemname, self.dbfile) as session:
            networks = session.query(NetworkSlots.NETWORK).distinct()
            return [item[0] for item in networks]

    def get_slots_list(self) -> list:
        with DBSession(self.systemname, self.dbfile) as session:
            slots = session.query(NetworkSlots.SLOT).distinct()
            return [item[0] for item in slots]

    def get_game_variables(self):
        with DBSession(self.systemname, self.dbfile) as session:
            vars = session.query(GameVariables.AWAY_TEAM,
            GameVariables.HOME_TEAM,
            GameVariables.WEEK, # string
            GameVariables.SLOT,
            GameVariables.NETWORK,
            GameVariables.QUAL_POINTS)
            return [(item[0],item[1],item[2], item[3], item[4], item[5]) for item in vars]

    def add_records(self, objects:list) -> None:
        with DBSession(self.systemname, self.dbfile) as session:
             session.add_all(objects)
    
