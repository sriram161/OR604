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
good_stores = server_obj.get_good_stores()
print('Total Shops: ', len(cfg['demand'].keys()), 'Total good Shops: ', len(good_stores), sep='\n')
