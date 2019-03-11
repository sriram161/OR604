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

#### Please uncomment below and run to create and load tables with data.
# create_tables(systemname, dbfile)
# load_production_table(data_path, milk_supply, systemname, dbfile)
# load_milkdemand_table(data_path, milk_demand, systemname, dbfile)
# load_cowfeed_table(data_path, feed_cost, systemname, dbfile)

#### Data preparation for optimization.
cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['milk_production'] = server_obj.get_milk_production() # gals/calving_cow for a demand month.s
cfg['feed_cost'] = server_obj.get_feed_cost()  #  $/cow-month.
cfg['milk_demand'] = server_obj.get_milk_demand() # gals for demand month.
cfg['milk_price'] = server_obj.get_milk_price() # $/gal.

import pprint
pprint.pprint(cfg)

#### GUROBI OPTIMIZATION MODEL.
dairy = grb.Model()
dairy.modelSense = grb.GRB.MINIMIZE

# Indices
demand_months = cfg['milk_demand'].keys()
calving_months = cfg['milk_price'].keys()

# Decision variables - 1 [Transportation integer] # No.of Cow calving cows for a demand month. 
no_cows = {}
# TODO: Re write the paper objective function to include cost of wasted milk.
for calvin_month in calving_months:
    for demand_month in demand_months:
         no_cows[demand_month, calvin_month] = dairy.addVar(
             obj=(
                 cfg['feed_cost'][demand_month, calvin_month] +
                 cfg['milk_production'][demand_month, calvin_month]),
            vtype= grb.GRB.INTEGER,
            name=f'ncow_D{demand_month}_C{calvin_month}')

# TODO: Create paper model constraints.

# ardent.update()
#Constraints
# my_constr = {}

#Availability constraint <no units>
# for mill in mills:
#    for center in centers:
#       cname = f'avail_{mill}_{center}'
#       my_constr[cname] = ardent.addConstr(
#          mill_transport_route[mill, center] <= mill_production[mill], name=cname)

# Center served by only 1 mill. <no units>
# for center in centers:
#       cname = f'serve_{center}'
#       my_constr[cname] = ardent.addConstr(grb.quicksum(
#           mill_transport_route[mill, center] for mill in mills) == 1,  name=cname)

# my supply constrain <cups>
# for mill in mills:
#       cname = f'supply_{mill}'
#       my_constr[cname] = ardent.addConstr(grb.quicksum(
#           3.33 * 50 * cfg['mill_supply_capacity'][mill] * mill_production[mill] - 
#           3.25 * cfg['center_demand'][center] * mill_transport_route[mill, center] for center in centers) >= 0,
#        name = cname)

dairy.update()
dairy.write('dairy.lp')

# ardent.optimize()
# ardent.update()

# for idx, item in enumerate(mill_production.items()):
#    if item[1].X != 0:
#       print(item[0], item[1].X)

# for idx, item in enumerate(mill_transport_route.items()):
#    if item[1].X != 0:
#       print(item[0], item[1].X)


#### OUTPUT RESULTS FILE.
# optimal_values = [Results(ID_=idx, CENTERID=item[0][0], STOREID=item[0][1], ROUTE=item[1].X)
#                   for idx, item in enumerate(mill_transport_route.items())]
# server_obj.add_records(optimal_values)
