import os

import pytest

from mindmap.models import Item


@pytest.fixture
def fixture_dir():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(test_dir, "fixtures")


@pytest.fixture
def mock_table_of_content_dict():
    root_item = Item("Root", href="./index.yml")
    children_item = Item("Children", parent=root_item)
    _ = Item("Test 1", parent=children_item, href="test-1.md")
    _ = Item("Test 2", parent=children_item, href="test-2.md")

    return root_item
