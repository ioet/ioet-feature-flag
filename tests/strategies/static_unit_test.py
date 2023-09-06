import pytest

from ioet_feature_flag.strategies import Static


class TestStaticStrategy:
    @pytest.mark.parametrize("is_enabled", [True, False])
    def test__returns_toggles_specified_in_attributes(
        self,
        is_enabled,
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "static",
        }
        static_strategy = Static.from_attributes(attributes)
        assert static_strategy.is_enabled() == is_enabled
