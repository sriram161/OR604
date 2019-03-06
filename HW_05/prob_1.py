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
create_tables(systemname, dbfile)
load_production_table(data_path, milk_supply, systemname, dbfile)
load_milkdemand_table(data_path, milk_demand, systemname, dbfile)
load_cowfeed_table(data_path, feed_cost, systemname, dbfile)

#### Data preparation for optimization.
# cfg = dict()

# server_obj = DataService(systemname, dbfile)

# cfg['flour_production_cost'] = server_obj.get_mill_flour_prouction_cost() # $/sacks
# cfg['center_trasport_cost'] = server_obj.get_center_transport_cost()  #  $/mile truck load.
# cfg['distance'] = server_obj.get_distances() # mile
# cfg['center_demand'] = server_obj.get_demand_center() # dough
# cfg['mill_supply_capacity'] = server_obj.get_mill_capacity() # sacks


#### GUROBI OPTIMIZATION MODEL.
# ardent = grb.Model()
# ardent.modelSense = grb.GRB.MINIMIZE

# Indices
# mills = cfg['flour_production_cost'].keys()
# centers = cfg['center_trasport_cost'].keys()

# cfg['mill_retool_cost'] = {mill : 700000 for mill in mills}

# Decision variables - 1 [Transportation integer] # truck load <$ = $ + $> convertions factor in doughs.
# mill_transport_route = {}
# for mill in mills:
#    for center in centers:
#          mill_transport_route[mill, center] = ardent.addVar(
#              obj=(
#                cfg['distance'][mill, center] * cfg['center_trasport_cost'][center] * (3.25/880*50*3.33) * cfg['center_demand'][center] +
#                cfg['flour_production_cost'][mill] * (3.25/(3.33*50)) * cfg['center_demand'][center]
#                ),
#             vtype= grb.GRB.BINARY,
#             name=f'transport_{mill}_{center}')

# Decision variables - 2 [Mill open or close binary]
# mill_production = {}
# for mill in mills:
#          mill_production[mill] = ardent.addVar(
#              obj=(
#                  cfg['mill_retool_cost'][mill]),
#              vtype=grb.GRB.BINARY,
#              name=f'cost_{mill}')

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

# ardent.update()
# ardent.write('ardent.lp')

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
