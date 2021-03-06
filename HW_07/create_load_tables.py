import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_game_variables_table
from app.db.onetimes import load_network_slot_week_table
from app.db.onetimes import load_team_data_table
from app.db.onetimes import load_opponents_table
import os
path_ = os.getcwd()
#### Please fix path if any error of file not found.
# NOTE: Always run the command from HW_06 folder.
data_path = path_ + "/app/data/"
dbfile = r'hw_07.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
game_variables = r'GAME_VARIABLES_2018_V1.csv'
network_slot_week = r'NETWORK_SLOT_WEEK_2018_V1.csv'
opponents = r'opponents_2018_V1.csv'
team_data = r'TEAM_DATA_2018_v1.csv'

# NOTE: If the program fails please delete hw_06.db and rerun the program.
# INFO: create tables.
create_tables(systemname, dbfile)

# INFO: load tables with data.
load_game_variables_table(data_path, game_variables, systemname, dbfile)
load_network_slot_week_table(data_path, network_slot_week, systemname, dbfile)
load_opponents_table(data_path, opponents, systemname, dbfile)
load_team_data_table(data_path, team_data, systemname, dbfile)
