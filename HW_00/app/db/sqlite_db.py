from .db_interface import Database
from sqlalchemy import create_engine

class SqliteDbEngine(Database):
    """ Sqlite dbEngine to manage sqlite database connection.
    """
    def __init__(self, dbfile, **kargs):
        self.db = create_engine("sqlite:///{}".format(dbfile), **kargs)

    def set_database(self, dbfile, **kargs):
        """ Cratea a sqlite database engine generator.
        """
        return SqliteDbEngine(dbfile, **kargs)

    def get_database(self):
        return self.db
