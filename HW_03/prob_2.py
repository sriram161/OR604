import numpy as np
import gurobipy as grb
from app.db.onetimes import create_tables
from app.db.onetimes import load_centers_table
from app.db.onetimes import load_goodstores_table
from app.db.onetimes import load_shopdemand_table
from app.services.data import DataService
from app.models.results import Results

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_03/app/data/"
dbfile = r'hw_03.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
shops = r"OR 604 Dominos Daily Demand.csv"
distribution_centers = r"Distributor_Data.csv"
good_shops = r"OR604 Good Dominos Data.csv"

#### Please uncomment below and run to create and load tables with data.
create_tables(systemname, dbfile)
load_centers_table(data_path, distribution_centers, systemname, dbfile)
load_goodstores_table(data_path, good_shops, systemname, dbfile)
load_shopdemand_table(data_path, shops, systemname, dbfile)

cfg = dict()

server_obj = DataService(systemname, dbfile)

cfg['distance'] = server_obj.get_distances()
cfg['cost'] = server_obj.get_cost()
cfg['demand'] = server_obj.get_demand()
cfg['capacity'] = server_obj.get_capacity()

good_stores = server_obj.get_good_stores()
stores_with_demand = set(cfg['demand'].keys())
new_stores = set(good_stores) - stores_with_demand
closed_stores = stores_with_demand - set(good_stores)

print(f"Total Stores: {len(cfg['demand'].keys())}", f'Total good Stores: {len(good_stores)}', \
      f'Total new_stores:{len(new_stores)}', f'Total closed_stores: {len(closed_stores)}', sep='\n')

# Remove closed stores.
for store in closed_stores:
    cfg['demand'].pop(store)

print(f"Total Stores after removal of old stores: {len(cfg['demand'])}")

for new_store in new_stores:
    if new_store not in cfg['demand'].keys():
       cfg['demand'][new_store] = -1

print(f"Total Stores after adding new_stores: {len(cfg['demand'])}")

total_proxy_demand_needed = sum(1 for _ in filter(lambda val: val == -1 ,cfg['demand'].values()))
print(f"Total proxy values needed: {total_proxy_demand_needed}")


#Assign average value to new stores
avg_across_demand = np.mean([_ for _ in filter(lambda val: val != -1 ,cfg['demand'].values())])
for new_store in new_stores:
       cfg['demand'][new_store] = avg_across_demand

# GRB model
dominos = grb.Model()
dominos.modelSense = grb.GRB.MINIMIZE
centers = cfg['cost'].keys()
stores = cfg['demand'].keys()

# Decision variables
dough_delivery = {}
for center in centers:
      for store in stores:
            dough_delivery[center, store] = dominos.addVar(obj=(cfg['distance'][center, store]*cfg['cost'][center])*2.0/9000, name=f'{center}_{store}')

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

optimal_values = [Results(CENTER_ID=item[0], STORE_NUMBER=item[1], DOUGHS_VALUE=value.X)
                  for item, value in dough_delivery.items()]
server_obj.add_records(optimal_values)
