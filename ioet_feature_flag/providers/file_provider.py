import abc
from pathlib import Path
import typing
import os

from ..exceptions import ToggleNotFoundError, ToggleEnvironmentError
from .provider import Provider


class FileBasedProvider(Provider, abc.ABC):
    def __init__(
        self,
        toggles_file_path: str,
        environment: typing.Optional[str] = None,
    ) -> None:
        self._path: Path = Path(toggles_file_path).resolve()
        self._environment = environment or os.getenv("ENVIRONMENT")
        self._validate_environment()

    @abc.abstractmethod
    def load_toggles_from_file(self, file_object: typing.IO) -> typing.Dict[str, typing.Dict]:
        raise NotImplementedError

    def _validate_environment(self):
        if not self._environment:
            raise ToggleEnvironmentError(
                "Could not retrieve toggles: Toggle environment not specified."
            )
        with open(self._path, "r") as toggles_file:
            toggles = self.load_toggles_from_file(toggles_file)
            environment_toggles: typing.Dict = toggles.get(self._environment)
            if not environment_toggles:
                raise ToggleEnvironmentError(
                    f"The environment {self._environment} was not found in the"
                    f" provided {self._path} toggles file."
                )

    def get_toggle_list(self) -> typing.List[str]:
        with open(self._path, "r") as toggles_file:
            toggles = self.load_toggles_from_file(toggles_file)
            environment_toggles: typing.Dict = toggles[self._environment]
            return list(environment_toggles.keys())

    def get_toggle_attributes(self, toggle_name: str) -> typing.Dict:
        with open(self._path, "r") as toggles_file:
            toggles = self.load_toggles_from_file(toggles_file)
            environment_toggles: typing.Dict = toggles.get(self._environment, {})
            toggle_attributes = environment_toggles.get(toggle_name)
            if not toggle_attributes:
                raise ToggleNotFoundError(
                    f"The toggle {toggle_name} was not found in the"
                    f" {self._environment} environment."
                )
            return toggle_attributes
