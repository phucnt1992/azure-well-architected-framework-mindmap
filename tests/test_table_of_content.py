import os

import pytest

from mindmap.models import Item, TableOfContent


@pytest.fixture
def mock_table_of_content_dict():
    root_item = Item("Root", href="./index.yml")
    children_item = Item("Children", parent=root_item)
    _ = Item("Test 1", parent=children_item, href="test-1.md")
    _ = Item("Test 2", parent=children_item, href="test-2.md")

    return root_item


def test_convert_table_of_content_to_object(mock_table_of_content_dict):
    # Act
    actual_result = TableOfContent()

    actual_result.convert_from_dict(
        {
            "name": "Root",
            "href": "./index.yml",
            "items": [
                {
                    "name": "Children",
                    "items": [
                        {"name": "Test 1", "href": "test-1.md"},
                        {"name": "Test 2", "href": "test-2.md"},
                    ],
                }
            ],
        }
    )

    # Assert
    assert str(actual_result) == str(TableOfContent(mock_table_of_content_dict))


def test_convert_table_of_content_to_mindmap(mock_table_of_content_dict):
    # Arrange
    test_dir = os.path.dirname(os.path.realpath(__file__))
    example_dir = os.path.join(test_dir, "examples")

    table_of_content = TableOfContent(mock_table_of_content_dict, example_dir)

    # Act
    actual_result = table_of_content.to_mindmap()

    # Assert
    with open(os.path.join(example_dir, "expected_result.md"), "r") as file:
        expected_result = file.read()
        assert actual_result == expected_result
