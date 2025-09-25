import os

import pytest

from mindmap.converters import MindMapConverter
from mindmap.models import Item, TableOfContent


def test_convert_table_of_content_to_mindmap_should_return_expected_result(
    mock_table_of_content_dict: Item,
) -> None:
    # Arrange
    test_dir = os.path.dirname(os.path.realpath(__file__))
    example_dir = os.path.join(test_dir, "examples")
    table_of_content = TableOfContent(mock_table_of_content_dict, root_dir=example_dir)
    converter = MindMapConverter(root_dir=example_dir, root_uri="/")

    # Act
    actual_result = converter.convert(table_of_content)

    # Assert
    with open(os.path.join(example_dir, "expected_result.md"), "r") as file:
        expected_result = file.read()
        assert actual_result == expected_result


@pytest.mark.skip(reason="Astro markdown format is under development")
def test_covert_table_of_content_to_astro_markdown_should_return_expected_result(
    mock_table_of_content_dict: Item,
) -> None:
    # Arrange
    test_dir = os.path.dirname(os.path.realpath(__file__))
    example_dir = os.path.join(test_dir, "examples")
    table_of_content = TableOfContent(mock_table_of_content_dict, root_dir=example_dir)
    converter = MindMapConverter(root_dir=example_dir, root_uri="/")

    # Act
    actual_result = converter.convert(table_of_content, astro_md=True)

    # Assert
    with open(os.path.join(example_dir, "expected_result_astro.md"), "r") as file:
        expected_result = file.read()
        assert actual_result == expected_result
