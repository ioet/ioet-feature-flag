import abc


class Strategy(abc.ABC):
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        raise NotImplementedError
