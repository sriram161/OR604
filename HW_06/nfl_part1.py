import numpy as np
import gurobipy as grb
from app.services.data import DataService

#### Please change path relative to your system.
data_path = r"c:/Users/notme/Documents/Development/OR604/HW_06/app/data/"
dbfile = r'hw_06.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
game_variables = r'GAME_VARIABLES_2018_V1.csv'
network_slot_week = r'NETWORK_SLOT_WEEK_2018_V1.csv'
team_data = r'TEAM_DATA_2018_v1.csv'
opponents = r'opponents_2018_V1.csv'

#### Data preparation for optimization.
cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['away'] = server_obj.get_away_dict()
cfg['home'] = server_obj.get_home_dict()
cfg['teams'] = server_obj.get_team_list()
#cfg['weeks']  dynamic
cfg['networks'] = server_obj.get_network_list()
cfg['slots'] = server_obj.get_slots_list()
cfg['game_variables'] = server_obj.get_game_variables()

# verify counts of the data to with quesion.
print('Count of away teams:',len(cfg['away']))
print('Count of home teams:', len(cfg['home']))
print('Count of total teams:', len(cfg['teams']))
print('Count of networks:', len(cfg['networks']))
print('Count of slots per week:', len(cfg['slots']))

#### GUROBI OPTIMIZATION MODEL.
nfl = grb.Model()
grb.Model()
nfl.modelSense = grb.GRB.MAXIMIZE
nfl.setParam('TimeLimit', 60)

# Indices
seasons = []

# Decision variables
games = {}
for a, h, w, s, n, q in cfg['game_variables']:
    cname=f'game_{a}_{h}_{w}_{s}_{n}'
    games[a, h, w, s, n] = nfl.addVar(obj=q, vtype=grb.GRB.BINARY, name=cname)
    seasons.append((a, h, w, s, n))
seasons = grb.tuplelist(seasons)

#Constraints
my_constr = {}

# Constraint-> 1: Each game played exaclty once.
for t in cfg['teams']:
    for h in cfg['away'][t]:
        cname = f'01_exactly_one_game_{t}_{h}'
        my_constr[cname] = nfl.addConstr(
        (games[t, h, w, s, n] for t, h, w, s, n in seasons.select(t, h, '*', '*', '*')) == 1,
        name = cname)
# Constraint-> 2: Team plays exacltly one game per week.(Count BYE as a game - where BYE is the home team)
# Constraint-> 3: Byes can only happen from week 4 and 12.
# Constraint-> 4: No more than 6 byes in a week.
# Constraint-> 5: No team that had a early bye (week 4) in 2017 can have an early bye game (week 4) in 2018. ?????
# Constraint-> 6: There is one Thursday Night game per week for weeks 1-15 and no thursday game in weeks 16 and 17.
# Constraint -> 7: There are 2 saturday night games each in week 15 and week 16(1 sate and satl each week)
nfl.update()
nfl.write('nfl.lp')
