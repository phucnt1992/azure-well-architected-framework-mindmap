from dataclasses import dataclass


@dataclass
class Item:
    NAME_FIELD = "name"
    HREF_FIELD = "href"
    ITEMS_FIELD = "items"

    name: str | int
    parent: "Item"
    children: list["Item"]
    href: str
    root_dir: str

    def __init__(
        self,
        name: str,
        parent: "Item" = None,
        href: str = None,
        root_dir: str = None,
    ):
        self.name = name
        self.href = href
        self.root_dir = root_dir
        self.children = []

        if parent is not None:
            self.parent = parent
            self.parent.add_child(self)

    def add_child(self, child: "Item"):
        child.parent = self
        self.children.append(child)


@dataclass
class TableOfContent:
    MAX_HEADER_LEVEL = 6
    NEW_LINE_CHAR = "\n"

    __root_dir: str
    root_item: Item

    def __init__(self, root: Item = None, root_dir: str = None, root_uri: str = "/"):
        self.root_item = root
        self.__root_dir = root_dir
        self.__root_uri = root_uri

    def __str__(self) -> str:
        return self.__str_recursive(self.root_item)

    def __str_recursive(self, item: Item, level: int = 0) -> str:
        result = f"{'  ' * level}- {item.name}{self.NEW_LINE_CHAR}"
        for child in item.children:
            result += self.__str_recursive(child, level + 1)

        return result

    def __has_items(self, item: dict) -> bool:
        return Item.ITEMS_FIELD in item and item[Item.ITEMS_FIELD] is not None

    def __load_items(self, items: list[dict], parent: Item) -> None:
        for item in items:
            new_item = Item(
                item.get(Item.NAME_FIELD),
                parent=parent,
                href=item.get(Item.HREF_FIELD, None),
                root_dir=self.__root_dir,
            )

            if self.__has_items(item):
                self.__load_items(item[Item.ITEMS_FIELD], new_item)

    def load(self, data: dict) -> None:
        self.root_item = Item(
            data.get(Item.NAME_FIELD),
            href=data.get(Item.HREF_FIELD, None),
            root_dir=self.__root_dir,
        )
        if self.__has_items(data):
            self.__load_items(data[Item.ITEMS_FIELD], self.root_item)

    def merge(self, other: "TableOfContent") -> "TableOfContent":
        if self.root_item is None:
            self.root_item = other.root_item
        else:
            self.root_item.add_child(other.root_item)

        return self
