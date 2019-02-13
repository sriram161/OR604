from sqlalchemy.sql.expression import literal
from sqlalchemy.orm import aliased
from app.models.location import Location
from app.models.trip import Trip
from app.services.computational.haver_vincenty import haversine_ #Question 3
from collections import defaultdict
from app.db.context import DBSession



# Question 1 and Question 2 record count check.
def count_records(systemname, dbfile):
    with DBSession(systemname, dbfile) as session:
        print('!!!! Location table count: ', session.query(Location).count())
        print('!!!! Trip table count: ',session.query(Trip).count())

# Question 4
def get_terminal_dist(systemname, dbfile) -> dict:
    location_alias = aliased(Location)
    dist_dict = defaultdict(None)
    with DBSession(systemname, dbfile) as session:
        for items in session.query(Location, location_alias).join(
                location_alias, literal(True)).all():
            items = sorted(items, key=lambda x: x.TERMINAL_NUMBER)
            dict_key = tuple(map(lambda x: x.TERMINAL_NUMBER, items))
            if dist_dict.get(dict_key):
                continue
            dist_dict[dict_key] = haversine_(
                (items[0].LATITUDE, items[0].LONGITUDE), (items[1].LATITUDE, items[0].LONGITUDE))
    return dist_dict
    
# Question 5
def get_neighbour_stations(data,source_terminal , dist) -> list:
    return list({ele for item in filter(lambda x: x[0] != x[1] and data[x] > dist ,data) for ele in item})

# Question 6
def get_trip_count(start_station, end_station, start_date, end_date, systemname='SqliteDbEngine', dbfile='precourse.db') -> int:
    with DBSession( systemname, dbfile) as session:
        return session.query(Trip)\
        .filter(Trip.START_STATION == start_station, Trip.STOP_STATION == end_station,
                Trip.START_DATE >= start_date, Trip.STOP_DATE <= end_date).count()
