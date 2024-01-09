import json
import typing

from ..exceptions import InvalidToggleFileFormat
from .file_provider import FileBasedProvider


class JsonToggleProvider(FileBasedProvider):
    """
    Provider for .json feature toggle files.

    This provider expects the file to have the following format

    {
        "yourEnvironment": {
            "yourToggleName": {
                "enabled": true,
                "type": "static"
            }
        }
    }

    You must set the `ENVIRONMENT` env variable and it must match
    `"yourEnvironment"`, otherwise it will throw an exception.
    """

    def load_toggles_from_file(self, file_object: typing.IO) -> typing.Dict[str, typing.Dict]:
        toggles = json.load(file_object)
        if not isinstance(toggles, typing.Dict):
            raise InvalidToggleFileFormat("The toggle file specified has an invalid format")
        return toggles
