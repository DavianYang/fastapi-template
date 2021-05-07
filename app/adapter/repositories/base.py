import abc


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    async def _create(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _update(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self):
        raise NotImplementedError
