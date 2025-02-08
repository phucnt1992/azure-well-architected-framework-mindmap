import os

from mindmap.utils.file import scan_toc_files


def test_scan_toc_files_with_empty_dir_should_return_empty_exception():
    # Arrange

    # Act
    actual_result = scan_toc_files("/dev/null")

    # Assert
    assert actual_result == []


def test_scan_toc_files_with_dir_with_index_yml_should_return_index_yml(fixture_dir):
    # Arrange

    # Act
    actual_result = scan_toc_files(fixture_dir, "test_index.yml")

    # Assert
    dir_path, file_path = actual_result[0]
    assert file_path == os.path.join(fixture_dir, "test_index.yml")
    assert dir_path == fixture_dir


def test_scan_toc_files_with_exclude_dir_should_return_empty_list(fixture_dir):
    # Arrange

    # Act
    actual_result = scan_toc_files(fixture_dir, "test_index.yml", "fixtures")

    # Assert
    assert actual_result == []
