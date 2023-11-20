from faker import Faker

import pytest


@pytest.fixture
def faker() -> Faker:
    return Faker()
