from vincenty import vincenty as vn 
from haversine import haversine as hv 

def check_input(inp):
    """
    """
    assert len(inp) == 2, 'Invalid number of values in point tuple'
    assert type(inp) is tuple, 'points must be in tuple'

def haversine_(point1, point2, unit='mi'):
    """ haversine value computation unit.
    """
    check_input(point1)
    check_input(point2)
    return hv(point1, point2, unit)

def vincenty_(point1,point2, miles=True):
    """ vincenty value computation unit.
    """
    check_input(point1)
    check_input(point2)
    return vn(point1, point2, miles)
