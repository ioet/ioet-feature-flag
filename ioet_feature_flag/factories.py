import typing
from .toggles import Toggles
from .providers import YamlToggleProvider, JsonToggleProvider, AWSAppConfigToggleProvider
from pathlib import Path

def _default_root_dir() -> Path:
    return Path(__file__).parent

def default_toggles() -> Toggles:
    return yaml_toggles()

def yaml_toggles(
    toggles_file_path: Path = Path("./feature_toggles/feature-toggles.yaml"),
    project_root_dir: typing.Optional[Path] = None,
) -> Toggles:
    provider = YamlToggleProvider(
        project_root_dir=project_root_dir or _default_root_dir(),
        toggles_file_path=toggles_file_path,
    )
    return Toggles(provider=provider)

def json_toggles(
    toggles_file_path: Path = Path("./feature_toggles/feature-toggles.json"),
    project_root_dir: typing.Optional[Path] = None,
) -> Toggles:
    provider = JsonToggleProvider(
        project_root_dir=project_root_dir or _default_root_dir(),
        toggles_file_path=toggles_file_path,
    )
    return Toggles(provider=provider)

def aws_appconfig_toggles() -> Toggles:
    provider = AWSAppConfigToggleProvider()
    return Toggles(provider=provider)
