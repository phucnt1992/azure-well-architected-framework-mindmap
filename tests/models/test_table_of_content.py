from mindmap.models import Item, TableOfContent


def test_table_of_content_when_init_should_set_properties():
    # Arrange
    root_item = Item("Root", href="./index.yml")

    # Act
    actual_result = TableOfContent(root_item)

    # Assert
    assert actual_result.root_item == root_item


def test_convert_table_of_content_to_object(mock_table_of_content_dict):
    # Act
    actual_result = TableOfContent()

    actual_result.load(
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


def test_merge_table_of_content():
    # Arrange
    first_toc = TableOfContent()
    first_toc.load(
        {
            "name": "First TOC",
            "href": "./index.yml",
        }
    )

    second_toc = TableOfContent()
    second_toc.load(
        {
            "name": "Second TOC",
            "href": "./index.yml",
            "items": [
                {
                    "name": "Children",
                    "items": [
                        {"name": "Test 3", "href": "test-3.md"},
                        {"name": "Test 4", "href": "test-4.md"},
                    ],
                }
            ],
        }
    )

    # Act
    actual_result = TableOfContent()
    actual_result.merge(first_toc).merge(second_toc)

    # Assert
    actual_result_content = str(actual_result)
    assert "First TOC" in actual_result_content
    assert "Second TOC" in actual_result_content
