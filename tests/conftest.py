import os

import pytest


@pytest.fixture
def fixture_dir():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(test_dir, "fixtures")
