from mindmap.models import Item


def test_item_when_init_should_set_properties():
    # Arrange
    name = "Test"
    parent = Item("Parent")
    href = "test.md"
    root_dir = "."

    # Act
    item = Item(name, parent, href, root_dir)

    # Assert
    assert item.name == name
    assert item.parent == parent
    assert item.href == href
    assert item.root_dir == root_dir
    assert item.children == []
