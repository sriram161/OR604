from sqlalchemy.ext.declarative import declarative_base

base = None
def get_base():
    global base
    if base is None:
        base = declarative_base()
    return base