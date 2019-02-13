""" 
@Description: OR604 pre course assignment to asses programming capabilities.
@Author: Sri Ram Sagar Kappagantula.
@Date: 4th Jan,2019.
"""

from app.db.onetimes import create_tables
from app.db.onetimes import load_location_table
from app.db.onetimes import load_trip_table
from app.solutions import count_records
from app.solutions import get_terminal_dist
from app.solutions import get_neighbour_stations
from app.solutions import get_trip_count

# Please change path relative to your system.
data_path = r"C:/Users/notme/Documents/Development/OR604_precourse/app/data/" # Please change path relative to your system.
dbfile = r'precourse_test.db' #Please give a new db file here.

# CONSTANTS
systemname = r'SqliteDbEngine'
zip_file = r'Capital_BikeShare_Data.zip'
location_file = r'Capital_Bike_Share_Locations.csv'

# Answer 1
create_tables(systemname, dbfile)

# Answer 2
load_location_table(data_path, location_file, systemname, dbfile)

load_trip_table(data_path, zip_file, systemname, dbfile)

# Answer 3
count_records(systemname, dbfile)

# Answer 4
dist_dict = get_terminal_dist(systemname, dbfile)

# Answer 5
neighbours = get_neighbour_stations(dist_dict, 31235, 5)
print('Total neighbours: ', len(neighbours))

# Answer 6
print('Total trips: ', get_trip_count(31222, 31235, '2011-01-01', '2011-09-01', systemname, dbfile))
