import os

from mindmap.utils import read_yml_file


def test_read_yml_file_with_invalid_file_should_return_none(fixture_dir):
    # Arrange
    empty_file = os.path.join(fixture_dir, "empty_index.yml")

    # Act
    actual_result = read_yml_file(empty_file)

    # Assert
    assert actual_result is None


def test_read_yml_file_with_valid_file_should_return_dict_content(fixture_dir):
    # Arrange
    test_file = os.path.join(fixture_dir, "test_index.yml")

    # Act
    actual_result = read_yml_file(test_file)

    # Assert
    assert bool(actual_result) is True
