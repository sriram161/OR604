import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_production_table
from app.db.onetimes import load_milkdemand_table
from app.db.onetimes import load_cowfeed_table
from app.services.data import DataService
from app.models.results import Optcows, Optmilk

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_06/app/data/"
dbfile = r'hw_06.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
milk_demand = r"demand_price.csv"
feed_cost = r"feedstock.csv"
milk_supply = r"production.csv"

#### Data preparation for optimization.
cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['milk_production'] = server_obj.get_milk_production() # gals/calving_cow for a demand month.s
cfg['feed_cost'] = server_obj.get_feed_cost()  #  $/cow-month.
cfg['milk_demand'] = server_obj.get_milk_demand() # gals for demand month.
cfg['milk_price'] = server_obj.get_milk_price() # $/gal.

#### GUROBI OPTIMIZATION MODEL.
dairy = grb.Model()
grb.Model()
dairy.modelSense = grb.GRB.MINIMIZE

# Indices
demand_months = range(1, 13)
calving_months = range(1, 13)

days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

# NOTE: Obj quciksum is not allowed in objective function.
# Decision variables - 1 [Transportation integer] # No.of Cow calving cows for a demand month. 
no_cows = {} # indexed by calving month.
excess_gals = {} # indexed by demand month.
shotage_gals = {} # indexed by demand month.

# INFO: Feed cost objective
for calvin_month in calving_months:
         no_cows[calvin_month] = dairy.addVar(
            obj=cfg['feed_cost'][calvin_month], vtype= grb.GRB.INTEGER,
            name=f'ncow_C{calvin_month}')

# INFO: excess objective
for demand_month in demand_months:
         excess_gals[demand_month] = dairy.addVar(
             obj=0.2*cfg['milk_price'][demand_month], vtype=grb.GRB.INTEGER,
            name=f'excess_C{demand_month}')

# INFO: shortage objective
for demand_month in demand_months:
         shotage_gals[demand_month] = dairy.addVar(
             obj=cfg['milk_price'][demand_month], vtype=grb.GRB.INTEGER,
            name=f'short_C{demand_month}')

#Constraints
my_constr = {}

# INFO: supply >= demand <excess>.
for demand_month in demand_months:
      cname = f'demand_{demand_month}'
      my_constr[cname] = dairy.addConstr(
          grb.quicksum(cfg['milk_production'][demand_month, calvin_month]*days[demand_month]*no_cows[calvin_month] for calvin_month in calving_months) -
          excess_gals[demand_month] +
          shotage_gals[demand_month] == cfg['milk_demand'][demand_month],
          name=cname)

dairy.update()
dairy.write('dairy_feed.lp')

dairy.optimize()
dairy.update()
dairy.write('dairy_feed.sol')

# OUTPUT: results stdout print.
for idx, item in enumerate(no_cows.items()):
   if item[1].X != 0:
      print(item[0], item[1].X)

print("excess...")
for idx, item in enumerate(excess_gals.items()):
   if item[1].X != 0:
      print(item[0], item[1].X)

print("shortage...")
for idx, item in enumerate(shotage_gals.items()):
   if item[1].X != 0:
      print(item[0], item[1].X)

#### OUTPUT RESULTS FILE.
# INFO: Considering feed cost.
optimal_values = [Optcows(ID_=idx, CALVINMONTH=item[0], COWCOUNT=item[1].X)
                  for idx, item in enumerate(no_cows.items())]
server_obj.add_records(optimal_values)

optimal_values_ = [Optmilk(ID_=idx, DEMANDMONTH=item[0], MILK=item[1].X, FLAG='EXCESS')
                  for idx, item in enumerate(no_cows.items())]
server_obj.add_records(optimal_values_)

optimal_values = [Optmilk(ID_=idx, DEMANDMONTH=item[0], MILK=item[1].X, FLAG='SHORTAGE')
                  for idx, item in enumerate(no_cows.items(), start=len(optimal_values_))]
server_obj.add_records(optimal_values)
