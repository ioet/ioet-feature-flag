import abc
import typing


class Provider(abc.ABC):
    @abc.abstractmethod
    def get_toggle_list(self) -> typing.List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_toggle_attributes(self, name: str) -> typing.Dict:
        raise NotImplementedError
