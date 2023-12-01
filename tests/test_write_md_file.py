import os
import shutil

import pytest

from mindmap.utils import write_md_file


@pytest.fixture
def temp_readme_file():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(test_dir, "output")
    readme_file = os.path.join(output_dir, "README.md")

    yield readme_file

    shutil.rmtree(output_dir)


@pytest.mark.usefixtures("temp_readme_file")
def test_write_md_file_should_return_file_with_content(temp_readme_file):
    # Arrange
    content = """
    # Hello World
    This is readme file.
    """

    # Act
    write_md_file(content, temp_readme_file)

    # Assert
    assert os.path.exists(temp_readme_file) is True
    assert os.path.getsize(temp_readme_file) > 0
    with open(temp_readme_file, "r") as file:
        assert content == file.read()


@pytest.mark.usefixtures("temp_readme_file")
def test_write_md_file_with_metadata_should_return_file_with_content_and_metadata(
    temp_readme_file,
):
    # Arrange
    meta = """---
    markmap:
      colorFreezeLevel: 2
      maxWidth: 300
      initialExpandLevel: 2
    ---"""

    content = """
    # Hello World
    This is readme file.
    """

    # Act
    write_md_file(content, temp_readme_file, meta)

    # Assert
    assert os.path.exists(temp_readme_file) is True
    assert os.path.getsize(temp_readme_file) > 0
    with open(temp_readme_file, "r") as file:
        assert meta + "\n\n" + content == file.read()
