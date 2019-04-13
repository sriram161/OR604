import numpy as np
import gurobipy as grb
from app.services.data import DataService
from app.models.results import Schedule
import os
path_ = os.getcwd()

# NOTE: Always run the command from HW_06 folder.
data_path = path_ + "/app/data/"
dbfile = r'hw_08.db'  # Please give a new db file here.

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
cfg['opponents'] = server_obj.get_opponents()
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
                      for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), w, '*', '*')) +
         grb.quicksum(games[a, t, w, s, n]
                      for a, t, w, s, n in seasons.select(list(cfg['home'][t]), t, w, '*', '*'))) == 1,
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

for i in range(1, 16):
        for w in range(i, i+3):        
                cname = f'08b_NoConsictDoubleHeaders_{w}'
                w = str(w)
                my_constr[cname] = nfl.addConstr(
                (grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select('*', '*', w, 'SUND', ['CBS', 'FOX']))) <= 2,
                name=cname)

for w in [17]:        
        cname = f'08c_DoubleHeaderInWeek_{w}'
        w = str(w)
        my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
                        for t, h, w, s, n in seasons.select('*', '*', w, 'SUND', ['CBS', 'FOX']))) == 1,
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
# ANSWER: Team playing home.
# select * from gamevariables where HOME_TEAM='LAC' and SLOT='MONN'; 
# NOTE: NO game variables for LAC in week 1.

cname = f'10b_MondayNightGameHostedByWestCoastMountain'
my_constr[cname] = nfl.addConstr(
        (grb.quicksum(games[t, h, w, s, n]
                      for t, h, w, s, n in seasons.select('*', ['LAC', 'SF', 'SEA', 'OAK', 'LAR', 'DEN', 'ARI'], '1', 'MONN', '*'))) >= 1,
        name=cname)

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


# Constraint-> 11 No team plays 4 consecutive home/away games in a season (Bye is away game) 
for t in cfg['teams']:
        for i in range(1, 15):
                cname = f'11_No4ConsecutiveGamesAway_{t}_start_week_{i}'
                my_constr[cname] = nfl.addConstr(
                grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), [str(w) for w in range(i, i+4)], '*', '*'))                                
                <= 3, name=cname)

for t in cfg['teams']:
        for i in range(1, 15):
                cname = f'11_No4ConsecutiveGamesHome_{t}_start_week_{i}'
                my_constr[cname] = nfl.addConstr(
                grb.quicksum(games[t, h, w, s, n]
                                for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, [str(w) for w in range(i, i+4)], '*', '*'))
                <= 3, name = cname)

# Constraint-> 12 No team plays 3 consecutive home/away games in weeks 1, 2, 3, 4, 5 and 15, 16, 17.
for t in cfg['teams']:
        cname = f'12_No3ConsecutiveGamesAway_{t}'
        for i in [1, 2, 3, 15]:
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                  for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), [str(w) for w in range(i, i+3)], '*', '*'))
                    <= 2,
                    name=cname)

for t in cfg['teams']:
        cname = f'12_No3ConsecutiveGamesHome_{t}'
        for i in [1, 2, 3, 15]:
                my_constr[cname] = nfl.addConstr(
                grb.quicksum(games[t, h, w, s, n]
                                  for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, [str(w) for w in range(i, i+3)], '*', '*'))
                    <= 2,
                    name=cname)


# Constraint-> 13 Each team must play at least 2 home/away games every 6 weeks (5 points).
for t in cfg['teams']:
        cname = f'13_Atleast2Away_{t}'
        for i in range(1, 12):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), [str(w) for w in range(i, i+6)], '*', '*'))
                    >= 2,
                    name=cname)

for t in cfg['teams']:
        cname = f'13_Atleast2Home_{t}'
        for i in range(1, 12):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, [str(w) for w in range(i, i+6)], '*', '*'))
                    >= 2,
                    name=cname)

# Constraint-> 14 Each team must play at least 4 homw/away games every 6 weeks
for t in cfg['teams']:
        cname = f'14_Atleast2Away_{t}'
        for i in range(1, 8):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), [str(w) for w in range(i, i+10)], '*', '*'))
                    >= 4,
                    name=cname)

for t in cfg['teams']:
        cname = f'14_Atleast2Home_{t}'
        for i in range(1, 8):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, [str(w) for w in range(i, i+10)], '*', '*'))
                    >= 4,
                    name=cname)
# Constraint-> 15 All tesams playing away on Thrsday nigh are homw the week before.
for t in cfg['teams']:
        cname = f'15_ThunAwayHomeWeekBefore_{t}'
        for w in range(2, 16):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w-1), '*', '*'))
                    <= 2,
                    name=cname)

# Constraint-> 16 Any team playing on Monday night in a given week cannot play Thursday night the next two weeks.
for t in cfg['teams']:
        cname = f'16_ThunAwayHomeWeekBefore_{t}'
        for w in range(1, 16):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w), 'MONN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w), 'MONN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w+1), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w+1), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w+2), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w+2), 'THUN', '*')) 
                    <= 1,
                    name=cname)

# Constraint-> 17 All teams playing on Thursday night in a given week will play home the previous week.
for t in cfg['teams']:
        cname = f'17_ThursdayNightPrevWeekHome_{t}'
        for w in range(2, 18):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w), 'THUN', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w-1), '*', '*'))
                    <= 2,
                    name=cname)
                
# Constraint-> 18 No team coming off of a BYE can play Thursday night
for t in cfg['teams']:
        cname = f'18_TeamByeCannotPlayThursdayNight_{t}'
        for w in range(4, 13):
                my_constr[cname] = nfl.addConstr(
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, 'BYE', str(w), '*', '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(t, list(cfg['away'][t]), str(w+1), ['THUE', 'THUL', 'THUN'], '*')) +
                    grb.quicksum(games[t, h, w, s, n]
                                 for t, h, w, s, n in seasons.select(list(cfg['home'][t]), t, str(w+1), ['THUE', 'THUL', 'THUN'], '*'))
                    <= 1,
                    name=cname)

# Constraint-> 19 Week 17 games can only consist of games between division opponents.
for a, h in cfg['opponents']: # Same divison zero.
        cname = f'19_GamesBetweenDivisonTeam_{w}_{a}_{h}'
        my_constr[cname] = nfl.addConstr(
                grb.quicksum(games[a, h, w, s, n]
                                for a, h, w, s, n in seasons.select(a, h, "17", '*', '*') 
                             if cfg['teams'][a][1] == cfg['teams'][h][1] and cfg['teams'][a][0] == cfg['teams'][h][0])
                >= 0,
                name=cname)

# Constraint-> 20 No team playing Thursday night on the road should trave more than 1 time zone away.
for t in cfg['teams']:
        cname = f'20_ThuNOnRoad1TimeZone_{t}'
        my_constr[cname] = nfl.addConstr(
                grb.quicksum(games[a, h, w, s, n]
                                for a, h, w, s, n in seasons.select(t, cfg['home'][t], '*', 'THUN', '*') 
                             if abs(cfg['teams'][a][2] == cfg['teams'][h][2]) <= 1) 
                >= 0,
                name=cname)

# Constraint-> 21 No team plays more than 2 toad games aganins teams coming off a BYE.
#linking variable
link = {}
for t in cfg['teams']:
        for h in cfg['away'][t]:
                for w in range(1, 18):
                        cname = f"link_{t}_{h}_{w}"
                        link[a, h, w] = nfl.addVar(obj=1, vtype=grb.GRB.BINARY, name=cname)

for t in cfg['teams']:
        for w in range(2, 18):
                cname = f'21_NoTeamPlay2GamesComingOffBye_{t}_{w}'
                my_constr[cname] = nfl.addConstr(
                        grb.quicksum(games[a, h, w, s, n]
                                        for a, h, w, s, n in seasons.select(t, cfg['home'][t], str(w), '*', '*')) +
                        grb.quicksum(games[a, h, w, s, n]
                                        for a, h, w, s, n in seasons.select(cfg['home'][t], 'BYE', str(w-1), 'SUNB', 'BYE')) -
                        grb.quicksum(link[a, h, w] for h in cfg['home'][t])
                        <= 1,
                        name=cname)

# Constraint-> 22 Division opponents cannot paly each other.
# a Back to back.
# b Gapped with a BYE.
# Constraint-> 23 Teams should not play 3 consecutive home/away games between weeks 4 through 16.
# Constraint-> 24 No team should play consecutive road games involving travel across more t han 1 time zone.
# Constraint-> 25 No team should open the season with two away games.
# Constraint-> 26 No team should end the season with two away games.
# Constraint-> 27 Florida teams should not play Early home games in the month of SEPT.
# Constraint-> 28 CBS and FOX should not have fewer than 5 games than each on a sunday. if it does happen, it cna only happen once in the season for each network.
# Constraint-> 29 CBS and FOX should not lose both games between divisional opponents for their assigned conference(FOX is assigned NFC, CBS is assigned AFC).
# Constraint-> 30 The searies between two divisional opponents should not end in the first half of the season(Weeks 1 through 9).
# Constraint-> 31 Teams should not play on the road the week following a Monday night game.

nfl.update()
nfl.write('nfl.lp')

nfl.optimize()
nfl.update()

# print("schedule...!!!")
# for idx, item in enumerate(games.items()):
#    if item[1].X != 0:
#       print(item[0], item[1].X)

# optimal_values = [Schedule(ROW_ID=idx, 
#                   AWAY_TEAM=item[0][0], 
#                   HOME_TEAM=item[0][1], 
#                   WEEK=item[0][2],
#                   SLOT=item[0][3],
#                   NETWORK=item[0][4],
#                   GAME_FLAG=item[1].X)
#                   for idx, item in enumerate(games.items())]
# server_obj.add_records(optimal_values)
