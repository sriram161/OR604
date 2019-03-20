import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_production_table
from app.db.onetimes import load_milkdemand_table
from app.db.onetimes import load_cowfeed_table
from app.services.data import DataService
from app.models.results import Optcows, Optmilk

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_05/app/data/"
dbfile = r'hw_05.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
milk_demand = r"demand_price.csv"
feed_cost = r"feedstock.csv"
milk_supply = r"production.csv"

# INFO: create tables.
create_tables(systemname, dbfile)

# INFO: load tables with data.
load_production_table(data_path, milk_supply, systemname, dbfile)
load_milkdemand_table(data_path, milk_demand, systemname, dbfile)
load_cowfeed_table(data_path, feed_cost, systemname, dbfile)
