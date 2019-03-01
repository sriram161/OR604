import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_centers_table
from app.db.onetimes import load_mills_table
from app.db.onetimes import load_shopdemand_table
from app.services.data import DataService
from app.models.results import Results

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_04/app/data/"
dbfile = r'hw_04.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
shops = r"average_daily_demand.csv"
distribution_centers = r"Distributor_Data.csv"
mills = r"Ardent_Mills_Data.csv"

#### Please uncomment below and run to create and load tables with data.
#create_tables(systemname, dbfile)
#load_shopdemand_table(data_path, shops, systemname, dbfile)
#load_centers_table(data_path, distribution_centers, systemname, dbfile)
#load_mills_table(data_path, mills, systemname, dbfile)

#### Data preparation for optimization.
cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['flour_production_cost'] = server_obj.get_mill_flour_prouction_cost()
cfg['center_trasport_cost'] = server_obj.get_center_transport_cost()  # Cost of trasport from mill to center.
cfg['distance'] = server_obj.get_distances()

cfg['center_demand'] = server_obj.get_demand_center()
cfg['mill_supply_capacity'] = server_obj.get_mill_capacity()

#### GUROBI OPTIMIZATION MODEL.
ardent = grb.Model()
ardent.modelSense = grb.GRB.MINIMIZE

# Indices
mills = cfg['flour_production_cost'].keys()
centers = cfg['center_trasport_cost'].keys()

cfg['mill_retool_cost'] = {mill : 70000 for mill in mills}

# Decision variables - 1 [Transportation integer] # counts in trucks
mill_transport_route = {}
for mill in mills:
   for center in centers:
         mill_transport_route[mill, center] = ardent.addVar(
             obj=(
               cfg['distance'][mill, center] * cfg['center_trasport_cost'][center]),
            vtype= grb.GRB.INTEGER,
            name=f'transport_{mill}_{center}')

# Decision variables - 2 [Mill open or close binary]
mill_production = {}
for mill in mills:
         mill_production[mill] = ardent.addVar(
             obj=(
                 cfg['flour_production_cost'][mill]*cfg['mill_supply_capacity'][mill] +
                 cfg['mill_retool_cost'][mill]),
             vtype=grb.GRB.BINARY,
             name=f'cost_{mill}')

ardent.update()
#Constraints
my_constr = {}

#Demand  # TODO demand -> doughs, Transport_route -> Truck 
# Trasport_route * 880 -> Sacks
# Scacks * 50 -> Pounds
# Pounds / 2 -> cup
# 1 Dough -> 3.25 cup
# Trasport_route * 880 * 50 -> pounds
# Trasport_route * 880 * 50 / 2 -> cups
# Trasport_route * 880 * 50 / 2 / 3.25 -> Doughs
for center in centers:
   cname = f'demand_{center}'
   my_constr[cname] = ardent.addConstr(grb.quicksum(
       (mill_transport_route[mill, center] * 880 * 50) / (2 * 3.25) for mill in mills) >= cfg['center_demand'][center], name=cname)  # TODO ask professor >= or ==.
#Supply constrains
for mill in mills:
   cname = f'supply_{mill}'
   my_constr[cname] = ardent.addConstr(grb.quicksum(
       mill_transport_route[mill, center] * 880 for center in centers) >= mill_production[mill] * cfg['mill_supply_capacity'][mill], name=cname)  # TODO ask professor >= or ==.

#Non negativity constrains
for mill in mills:
   for center in centers:
      cname = f'NonNegativity_{mill}'
      my_constr[cname] = ardent.addConstr(mill_transport_route[mill, center] >= 0, name=cname)  # TODO ask professor >= or ==.

"""
#Service only by one mill.  # supply -> unit/week is it truck loads per week? or sacks per week?
# 
for center in centers:
   cname = f'one_mill_{center}'
   my_constr[cname] = ardent.addConstr(grb.quicksum((route_exists[mill, center]) for mill in mills) == 1, name=cname)

# Supply and demand.
#for mill in mills:
#     my_constr[cname] = ardent.addConstr(grb.quicksum(
#      mill_transport_route[mill, center]*cfg['center_demand'][center] for center in centers) >= 
#      mill_production[mill]*cfg['mill_supply_capacity'][mill],
#      name=cname)
"""

ardent.update()
ardent.write('ardent.lp')

ardent.optimize()
ardent.update()
#import pdb; pdb.set_trace()

'''
#### OUTPUT RESULTS FILE.
optimal_values = [Results(ID_=idx ,CENTER_ID=item[0][0].replace('!', ' '), STORE_NUMBER=item[0][1], DOUGHS_VALUE=item[1].X)
                  for idx, item in enumerate(dough_delivery.items())]
server_obj.add_records(optimal_values)
'''
