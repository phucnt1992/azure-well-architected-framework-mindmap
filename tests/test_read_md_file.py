import os

from mindmap.models import read_md_file


def test_read_md_file_should_extract_headers_nodes(fixture_dir):
    # Arrange
    test_readme_file = os.path.join(fixture_dir, "test_readme.md")

    # Act
    actual_result = read_md_file(test_readme_file)

    # Assert
    assert actual_result == [
        "# Main Title",
        "## Header 1",
        "### Header 1.1",
        "#### Header 1.1.1",
        "## Header 2",
        "## Header 3",
        "### Header 3.1",
        "### Header 3.2",
        "## Header 4",
    ]
