from app.db.db_factory import DbFactory
from app.db.settings import get_base
from sqlalchemy.orm import sessionmaker
from app.db.db_factory import DbFactory

class DBSession(object):
    '''Context manager to handle database session'''

    def __init__(self, dbengine, dbfile):
        self.dbname = dbengine
        self.file = dbfile

    def __enter__(self):
        base = get_base()
        self.db = DbFactory.get_db_engine(
            self.dbname, self.file).get_database()
        self.session = sessionmaker(bind=self.db)()
        return self.session

    def __exit__(self, *args):
        self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()
