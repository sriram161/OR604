import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_production_table
from app.db.onetimes import load_milkdemand_table
from app.db.onetimes import load_cowfeed_table
from app.services.data import DataService
from app.models.results import Results

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_05/app/data/"
dbfile = r'hw_05.db'  # Please give a new db file here.

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
dairy.modelSense = grb.GRB.MINIMIZE

# Indices
demand_months = range(1, 13)
calving_months = range(1, 13)

# NOTE: Obj quciksum is not allowed in objective function.
# Decision variables - 1 [Transportation integer] # No.of Cow calving cows for a demand month. 
no_cows = {}
# INFO: Feed cost + excess milk objective function <Excess>.
for calvin_month in calving_months:
    for demand_month in demand_months:
         no_cows[calvin_month] = dairy.addVar(
             obj=(
                 0.2*cfg['milk_production'][demand_month, calvin_month] * cfg['milk_price'][demand_month]),
            vtype= grb.GRB.INTEGER,
            name=f'ncow_C{calvin_month}')

#Constraints
my_constr = {}

#Availability constraint <no units>
# NOTE: supply >= demand <excess>.
for demand_month in demand_months:
      cname = f'demand_{demand_month}'
      my_constr[cname] = dairy.addConstr(
          grb.quicksum(no_cows[calvin_month]*cfg['milk_production'][demand_month, calvin_month] for calvin_month in calving_months) >= cfg['milk_demand'][demand_month], name=cname)

dairy.update()
dairy.write('dairy_no_feed.lp')

dairy.optimize()
dairy.update()
dairy.write('dairy_no_feed.sol')

# OUTPUT results stdout print.
for idx, item in enumerate(no_cows.items()):
   if item[1].X != 0:
      print(item[0], item[1].X)

#### OUTPUT RESULTS FILE.
# INFO: Excluding feed cost.
optimal_values = [Results(ID_=idx, CALVINMONTH=item[0], COWCOUNT=item[1].X, SCENARIO='NO FEED')
                  for idx, item in enumerate(no_cows.items(), 13)]
server_obj.add_records(optimal_values)
