import os

from mindmap.converters import MindMapConverter
from mindmap.models import TableOfContent


def test_convert_table_of_content_to_mindmap(mock_table_of_content_dict):
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
