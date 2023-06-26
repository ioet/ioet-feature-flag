import abc

class Provider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_flag():
        raise NotImplementedError()

    @abc.abstractmethod
    def get_flag():
        raise NotImplementedError()
