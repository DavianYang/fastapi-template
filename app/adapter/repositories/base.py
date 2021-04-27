import abc

class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def _create(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _update(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _delete(self):
        raise NotImplementedError
        