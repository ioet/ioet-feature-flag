import typing
import yaml

from ._base_git_remote_provider import BaseGitRemoteProvider, DEFAULT_BASE_URL
from ...exceptions import InvalidToggleFileFormat


class YamlGitRemoteProvider(BaseGitRemoteProvider):
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
            extension="yaml",
            token=token,
            base_url=base_url,
            cache_ttl_seconds=cache_ttl_seconds,
        )

    def _load_toggles(self):
        self._toggles = yaml.safe_load(self._file_content)
        if not isinstance(self._toggles, dict):
            raise InvalidToggleFileFormat("The provided file doesn't have a valid YAML format.")
