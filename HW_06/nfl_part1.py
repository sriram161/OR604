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
# cfg['weeks']  dynamic
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
        cname = f'01_EachGameExaltlyOnce_{t}_{h}'
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
           for t, h, w, s, n in seasons.select(t, h, '*', '*', '*'))) == 1,
        name = cname)

# Constraint-> 2: Team plays exacltly one game per week.(Count BYE as a game - where BYE is the home team)
for t in cfg['away'].keys():
    for w in range(1,18):
        cname=f'02_ExactlyOneGamePerWeek_{t}_{w}'
        w=str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
            for t, h, w, s, n in seasons.select(t, '*', w, '*', '*')) +
         grb.quicksum(games[a, t, w, s, n]
            for a, t, w, s, n in seasons.select('*', t, w,'*', '*'))) == 1,
        name = cname)

# Constraint-> 3: Byes can only happen from week 4 and 12.
# QUESTION: Should I add bye games to games???
# INFO: BYE game for weeks 1-3 and 13-16 is not present in gamedata.
for w in range(4,13):
        cname = f'03_ByeOnlyWeek4and12_{w}'
        w=str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
             for t, h, w, s, n in seasons.select('*', 'BYE', w, '*', 'BYE'))) >= 1,
        name = cname)

# Constraint-> 4: No more than 6 byes in a week.
for w in range(4,13):
        cname = f'04_ByeGameLessThan6PerWeek_{w}'
        w=str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
             for t, h, w, s, n in seasons.select('*', 'BYE', w, '*', 'BYE'))) <= 6,
        name = cname)

# # Constraint-> 5: No team that had a early bye (week 4) in 2017 can have an early bye game (week 4) in 2018. ?????
for t in ['MIA', 'TB']:
        cname = f'05_earlyBye_{t}'
        w=str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
             for t, h, w, s, n in seasons.select(t, 'BYE', '4', '*', 'BYE'))) == 0,
        name = cname)

# Constraint-> 6: There is one Thursday Night game per week for weeks 1-15 and no thursday game in weeks 16 and 17.
for w in range(1,16):
        cname = f'06_1ThursdayNightPerWeek1To15_{w}'
        w=str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
             for t, h, w, s, n in seasons.select('*', '*', w, 'THUN', '*'))) == 1,
        name = cname)

for w in range(16, 18):
        cname = f'06_NoThursdayNightPerWeek16and17_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, 'THUN', '*'))) == 0,
            name=cname)

# Constraint-> 7: There are 2 saturday night games each in week 15 and week 16(1 sate and satl each week)
for w in range(15, 17):
     for s in ['SATL','SATE']:
        cname = f'07_TwoSaturdayGames_{w}_{s}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, s, '*'))) == 2,
            name=cname)

# Constraint-> 8: Sunday double header games.
for w in range(1, 17):
        cname = f'08a_SundayDoubleHeader_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, 'SUND', '*'))) == 1,
            name=cname)

for n in ['CBS', 'FOX']:
        for i in range(1, 16):
            for w in range(i, i+3):        
                cname = f'08b_NoConsictDoubleHeaders_{w}'
                w = str(w)
                my_constr[cname] = nfl.addConstr(
                (grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select('*', '*', w, 'SUND', n))) <= 2,
                name=cname)

for n in ['CBS', 'FOX']:
            for w in [17]:        
                cname = f'08c_DoubleHeaderInWeek_{w}_{n}'
                w = str(w)
                my_constr[cname] = nfl.addConstr(
                (grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select('*', '*', w, 'SUND', n))) == 1,
                name=cname)

# Constraint-> 9: Exactly one Sunday night game per week 1 to 16.

for w in range(1, 17):
        cname = f'09_OneSundayNightGame_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
                (grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select('*', '*', w, 'SUNN', '*'))) == 1,
                name=cname)

for w in [17]:
        cname = f'09_NoSundayNightGame_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, 'SUNN', '*'))) == 0,
            name=cname)

# Constraint-> 10: Monday night games.
for w in [1]:
        cname = f'10a_MondayNightGame_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
                        for t, h, w, s, n in seasons.select('*', '*', w, 'MONN', '*'))) == 2,
        name=cname)
# QUESTION: A team hosting means is it playing as away or home???
# for h in ['LAC', 'SF', 'SEA', 'OAK', 'LAR', 'DEN', 'ARI']:
#         cname = f'10b_MondayNightGameHostedByWestCoastMountain_{h}'
#         my_constr[cname] = nfl.addConstr(
#             (grb.quicksum(games[t, h, w, s, n]
#                           for t, h, w, s, n in seasons.select('*', h, '*', 'MONN', '*'))) >= 1,
#             name=cname)

for w in range(2, 17):
        cname = f'10c_ExacltyOneMondayNight_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, 'MONN', '*'))) == 1,
            name=cname)

for w in [17]:
        cname = f'10c_NoMondayNight_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
            (grb.quicksum(games[t, h, w, s, n]
                          for t, h, w, s, n in seasons.select('*', '*', w, 'MONN', '*'))) == 0,
            name=cname)

nfl.update()
nfl.write('nfl.lp')

nfl.optimize()
nfl.update()
