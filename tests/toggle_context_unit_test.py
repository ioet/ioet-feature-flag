import typing

import pytest
from faker import Faker

from ioet_feature_flag import ToggleContext


class TestGetMethod:
    def test__get_returs_username_role_and_custom_attributes(self, faker: Faker):
        test_data = {
            "username": faker.word(),
            "role": faker.word(),
            "custom_attribute_a": faker.pyint(),
        }
        context = ToggleContext(**test_data)

        username = context.get("username")
        role = context.get("role")
        custom_attribute = context.get("custom_attribute_a")

        assert username == test_data["username"]
        assert role == test_data["role"]
        assert custom_attribute == test_data["custom_attribute_a"]

    def test__get_returns_none_when_custom_attribute_not_found(self, faker: Faker):
        test_data = {"username": faker.word(), "role": faker.word()}
        context = ToggleContext(**test_data)

        custom_attribute = context.get("custom_attr")

        assert custom_attribute == None
