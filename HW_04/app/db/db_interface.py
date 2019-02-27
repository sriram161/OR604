import abc

class Database(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_database(self, dbfile: str, **kargs) -> object:
        pass

    def set_database(self) -> object:
        pass