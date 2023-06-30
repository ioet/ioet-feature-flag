from unittest.mock import mock_open
import json

from ioet_json_feature_flag.adapters.json_adapter import JSONAdapter


class TestJsonAdapter:
    def test_get_flags_when_there_is_a_file_returns_flags_dictionry(
        self, mocker, monkeypatch
    ):
        path = "configuration.json"
        expected_flags = {"flag_1": True, "flag_2": False}
        json_load_mock = mocker.Mock(return_value=expected_flags)
        mocker.patch(
            "ioet_json_feature_flag.adapters.json_adapter.open", new_callable=mock_open
        )
        monkeypatch.setattr(json, "load", json_load_mock)

        actual_flags = JSONAdapter(path).get_flags()

        assert expected_flags == actual_flags

    def test_get_flags_when_there_is_no_file_returns_empty_dictionary(self, mocker):
        path = "configuration.json"
        mocker.patch(
            "ioet_json_feature_flag.adapters.json_adapter.open",
            side_effect=FileNotFoundError,
        )

        actual_flags = JSONAdapter(path).get_flags()

        assert {} == actual_flags

    def test_set_flag_when_file_exists_then_returns_updated_flags(
        self, mocker, monkeypatch
    ):
        path = "configuration.json"
        outdated_flags = {"flag_1": True, "flag_2": False}
        expected_flags = {"flag_1": False, "flag_2": False}
        json_load_mock = mocker.Mock(return_value=outdated_flags)
        json_dump_mock = mocker.Mock()
        mocker.patch(
            "ioet_json_feature_flag.adapters.json_adapter.open", new_callable=mock_open
        )
        monkeypatch.setattr(json, "load", json_load_mock)
        monkeypatch.setattr(json, "dump", json_dump_mock)

        actual_flags = JSONAdapter(path).set_flag("flag_1", False)

        json_dump_mock.assert_called()
        assert expected_flags == actual_flags

    def test_set_flag_when_file_not_exists_then_returns_new_flags(
        self, mocker, monkeypatch
    ):
        path = "configurations.json"
        expectred_flags = {"new_flag": True}
        mocker.patch("builtins.open", new_callable=mock_open())
        json_load_mock = mocker.Mock(side_effect=FileNotFoundError)
        monkeypatch.setattr(json, "load", json_load_mock)
        json_dump_mock = mocker.Mock()
        monkeypatch.setattr(json, "dump", json_dump_mock)

        actual_flags = JSONAdapter(path).set_flag("new_flag", True)

        json_dump_mock.assert_called()
        assert expectred_flags == actual_flags
