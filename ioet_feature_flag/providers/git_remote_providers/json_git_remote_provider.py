import typing
import json

from ._base_git_remote_provider import BaseGitRemoteProvider, DEFAULT_BASE_URL
from ...exceptions import InvalidToggleFileFormat


class JsonGitRemoteProvider(BaseGitRemoteProvider):
    def __init__(
        self,
        project_id: str,
        environment: str,
        token: typing.Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        cache_ttl_seconds: int = 300,
    ):
        super().__init__(
            project_id=project_id,
            environment=environment,
            extension="json",
            token=token,
            base_url=base_url,
            cache_ttl_seconds=cache_ttl_seconds,
        )

    def _load_toggles(self):
        try:
            self._toggles = json.loads(self._file_content)
        except json.decoder.JSONDecodeError:
            raise InvalidToggleFileFormat("The provided file doesn't have a valid JSON format.")
