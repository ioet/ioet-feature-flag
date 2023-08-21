import pytest

from ioet_feature_flag.strategies.static import build_static_type


class TestStaticStrategy:
    @pytest.mark.parametrize("is_enabled", [True, False])
    def test__returns_toggles_specified_in_metadata(
        self,
        is_enabled,
    ):
        metadata = {
            "enabled": is_enabled,
            "type": "static",
        }
        static_strategy = build_static_type(metadata)

        assert static_strategy.is_enabled() == is_enabled
