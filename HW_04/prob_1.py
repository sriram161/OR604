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

cfg['mill_trasport_cost'] = server_obj.get_mill_transport_cost()  # Cost of trasport from mill to center.
cfg['center_demand'] = server_obj.get_center_capacity()
cfg['distance'] = server_obj.get_distances()
cfg['mill_supply_capacity'] = server_obj.get_mill_capacity()
import pdb; pdb.set_trace()

#### GUROBI OPTIMIZATION MODEL.
ardent = grb.Model()
ardent.modelSense = grb.GRB.MINIMIZE

# Indices
mills = cfg['mill_trasport_cost'].keys()
centers = cfg['center_demand'].keys()

# Decision variables
flour_delivery = {}
for mill in mills:
      for center in centers:
            flour_delivery[mill, center] = ardent.addVar(obj=(cfg['distance'][mill, center]*cfg['mill_trasport_cost'][mill])*2.0, name=f'{mill}_{center}')

ardent.update()
ardent.write('ardent.lp')

'''
#Constraints
my_constr = {}

for center in centers:
   cname = f'{center}'
   my_constr[cname] = dominos.addConstr(grb.quicksum(dough_delivery[center, store] for store in stores) <= cfg['capacity'][center], name=cname)

for store in stores:
   cname = f'{store}'
   my_constr[cname] = dominos.addConstr(grb.quicksum(dough_delivery[center, store] for center in centers) >= cfg['demand'][store], name=cname)

dominos.update()
dominos.write('dominos.lp')

dominos.optimize()
dominos.update()

#### OUTPUT RESULTS FILE.
optimal_values = [Results(ID_=idx ,CENTER_ID=item[0][0].replace('!', ' '), STORE_NUMBER=item[0][1], DOUGHS_VALUE=item[1].X)
                  for idx, item in enumerate(dough_delivery.items())]
server_obj.add_records(optimal_values)
'''
