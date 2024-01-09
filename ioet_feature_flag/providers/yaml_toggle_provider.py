from typing import Dict
import yaml
import typing

from ..exceptions import InvalidToggleFileFormat
from .file_provider import FileBasedProvider


class YamlToggleProvider(FileBasedProvider):
    """
    Provider for .yaml feature toggle files.

    This provider expects the file to have the following format

    your_environment:
        your_toggle_name:
            enabled: true
            type: static

    You must set the `ENVIRONMENT` env variable and it must match
    `"your_environment"`, otherwise it will throw an exception.
    """

    def load_toggles_from_file(self, file_object: typing.IO) -> Dict[str, Dict]:
        toggles = yaml.safe_load(file_object)
        if not isinstance(toggles, typing.Dict):
            raise InvalidToggleFileFormat("The toggle file specified has an invalid format")
        return toggles
