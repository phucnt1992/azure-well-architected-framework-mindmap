from mindmap.utils import remove_chars


def test_remove_chars_should_remove_selected_chars():
    # Arrange

    # Act
    actual_result = remove_chars("H(e)llo: W(o)r'l'd!")

    # Assert
    assert actual_result == "Hello World!"
