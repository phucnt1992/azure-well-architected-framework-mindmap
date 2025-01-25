from mindmap.utils import format_to_markdown_link


def test_format_to_markdown_link_should_return_md_link():
    # Arrange
    root_uri = "https://example.com/"
    href = "test.md"
    header = "#Test Header"
    level = 2

    # Act
    actual_result = format_to_markdown_link(root_uri, href, header, level)

    # Assert
    assert actual_result == " [Test Header](https://example.com/test#test-header)"
