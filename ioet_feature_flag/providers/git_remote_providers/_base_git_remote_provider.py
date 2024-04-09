import abc
import typing
from urllib import parse as urllib_parse
import requests
from cachetools import cachedmethod, TTLCache

from ...exceptions import InvalidToggleFileFormat, ToggleNotFoundError
from ..provider import Provider

DEFAULT_BASE_URL = "https://raw.githubusercontent.com/ioet/feature-flag-management/main/"


class BaseGitRemoteProvider(Provider, abc.ABC):
    def __init__(
        self,
        project_id: str,
        environment: str,
        extension: str,
        token: typing.Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        cache_ttl_seconds: int = 300,
    ) -> None:
        self._project_id = project_id
        self._base_url = base_url
        self._extension = extension
        self._environment = environment
        self._token = token
        self._file_content = None
        self._toggles = {}
        self.cache_ttl = TTLCache(maxsize=float("inf"), ttl=cache_ttl_seconds)

    @cachedmethod(lambda self: self.cache_ttl)
    def _load_file_content(self):
        """
        Considerations:

        This function is being cached to prevent performing an HTTP request
        every time it gets called in a short period of time.
        However, we don't want to permanently cache it either, because if a toggle
        changes in the remote repository, the change wouldn't be reflected
        until the application is reloaded.
        """
        url = urllib_parse.urljoin(
            self._base_url,
            f"{self._project_id}/{self._environment}.{self._extension}",
        )
        headers = None
        if self._token:
            headers = {"Authorization": f"token {self._token}"}
        response = requests.request(
            method="GET",
            url=url,
            headers=headers,
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise InvalidToggleFileFormat(f"Unable to load toggles file from remote: {str(e)}")

        self._file_content = response.text
        if not self._file_content:
            raise InvalidToggleFileFormat("The provided file is empty.")

    @abc.abstractmethod
    def _load_toggles(self):
        raise NotImplementedError()

    def get_toggle_list(self) -> typing.List[str]:
        self._load_file_content()
        self._load_toggles()
        return list(self._toggles.keys())

    def get_toggle_attributes(self, toggle_name: str) -> typing.Dict:
        self._load_file_content()
        self._load_toggles()
        toggle_attributes = self._toggles.get(toggle_name)
        if not toggle_attributes:
            raise ToggleNotFoundError(
                f"The toggle {toggle_name} was not found."
            )
        return toggle_attributes
