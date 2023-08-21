import pytest


from ioet_feature_flag.strategies import get_toggle_strategy
from ioet_feature_flag.strategies import Static
from ioet_feature_flag.strategies import Cutover
from ioet_feature_flag.exceptions import InvalidToggleType


@pytest.mark.parametrize(
    "metadata, expected_result, expected_exception",
    [
        ({"type": "static"}, Static, None),
        ({"type": "cutover", "date": "2023-08-21 08:00"}, Cutover, None),
        ({"type": "non_existent_type"}, None, InvalidToggleType),
    ]
)
def test_get_toggle_strategy(metadata, expected_result, expected_exception):
    metadata["enabled"] = True
    if expected_exception:
        with pytest.raises(expected_exception):
            get_toggle_strategy(metadata)
    else:
        strategy = get_toggle_strategy(metadata)
        assert isinstance(strategy, expected_result)
