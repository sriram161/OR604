import abc

class Database(metaclass=abc.ABCMeta):
    """ Interface for databases.
    """

    @abc.abstractmethod
    def get_database(self, dbfile: str, **kargs) -> object:
        pass

    def set_database(self) -> object:
        pass