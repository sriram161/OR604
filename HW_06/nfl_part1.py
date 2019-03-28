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
opponents = r'opponents_2018_V1.csv'
team_data = r'TEAM_DATA_2018_v1.csv'

#### Data preparation for optimization.
cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['milk_production'] = server_obj.get_milk_production() # gals/calving_cow for a demand month.s
cfg['feed_cost'] = server_obj.get_feed_cost()  #  $/cow-month.
cfg['milk_demand'] = server_obj.get_milk_demand() # gals for demand month.
cfg['milk_price'] = server_obj.get_milk_price() # $/gal.

#### GUROBI OPTIMIZATION MODEL.
nfl = grb.Model()
grb.Model()
nfl.modelSense = grb.GRB.MAXIMIZE

# Indices

# Decision variables
