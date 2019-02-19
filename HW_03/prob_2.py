from app.db.onetimes import create_tables
from app.db.onetimes import load_centers_table
from app.db.onetimes import load_goodstores_table
from app.db.onetimes import load_shopdemand_table

#### Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604/HW_03/app/data/"
dbfile = r'hw_03.db'  # Please give a new db file here.

#### CONSTANTS
systemname = r'SqliteDbEngine'
shops = r"OR 604 Dominos Daily Demand.csv"
distribution_centers = r"Distributor_Data.csv"
good_shops = r"OR604 Good Dominos Data.csv"


#### Please uncomment below and run to create and load tables with data.
#create_tables(systemname, dbfile)
#load_centers_table(data_path, distribution_centers, systemname, dbfile)
#load_goodstores_table(data_path, good_shops, systemname, dbfile)
#load_shopdemand_table(data_path, shops, systemname, dbfile)

cfg = dict()

from app.services.data import DataService

server_obj = DataService(systemname, dbfile)
cfg['cost'] = server_obj.get_cost()
cfg['capacity'] = server_obj.get_capacity()
cfg['demand'] = server_obj.get_demand()
cfg['distance'] = server_obj.get_distances()

good_stores = server_obj.get_good_stores()
stores_with_demand = set(cfg['demand'].keys())
new_stores = set(good_stores) - stores_with_demand
closed_stores = stores_with_demand - set(good_stores)
print(f"Total Stores: {len(cfg['demand'].keys())}", f'Total good Stores: {len(good_stores)}', \
      f'Total new_stores:{len(new_stores)}', f'Total closed_stores: {len(closed_stores)}', sep='\n')

for store in closed_stores:
    cfg['demand'].pop(store)

print(f"Total Stores after removal of old stores: {len(cfg['demand'])}")

for new_store in new_stores:
    if new_store not in cfg['demand'].keys():
       cfg['demand'][new_store] = -1

print(f"Total Stores after adding new_stores: {len(cfg['demand'])}")

total_proxy_demand_needed = sum(1 for _ in filter(lambda val: val == -1 ,cfg['demand'].values()))
print(f"Total proxy values needed: {total_proxy_demand_needed}")

