import os

from mindmap.utils import load_indexes


def test_load_indexes_with_empty_dir_should_return_empty_exception():
    # Arrange

    # Act
    actual_result = load_indexes("/dev/null")

    # Assert
    assert actual_result == []


def test_load_indexes_with_dir_with_index_yml_should_return_index_yml(fixture_dir):
    # Arrange

    # Act
    actual_result = load_indexes(fixture_dir, "test_index.yml")

    # Assert
    dir_path, file_path = actual_result[0]
    assert file_path == os.path.join(fixture_dir, "test_index.yml")
    assert dir_path == fixture_dir
