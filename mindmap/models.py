import logging
from dataclasses import dataclass

from mindmap.utils.file import NEW_LINE_CHAR

logger = logging.getLogger(__name__)


@dataclass
class Item:
    NAME_FIELD = "name"
    HREF_FIELD = "href"
    ITEMS_FIELD = "items"

    name: str
    parent: "Item | None"
    children: list["Item"]
    href: str
    root_dir: str | None

    def __init__(
        self,
        name: str,
        parent: "Item | None" = None,
        href: str | None = None,
        root_dir: str | None = None,
    ):
        self.name = name
        self.href = href if href is not None else ""
        self.root_dir = root_dir
        self.children = []

        if parent is None:
            self.parent = None
        else:
            self.parent = parent
            self.parent.add_child(self)

    def add_child(self, child: "Item"):
        child.parent = self
        self.children.append(child)


@dataclass
class TableOfContent:

    __root_dir: str | None
    __root_item: Item | None

    def __init__(self, root: Item | None = None, root_dir: str | None = None):
        self.__root_item = root
        self.__root_dir = root_dir

    @property
    def root_item(self) -> Item | None:
        return self.__root_item

    @root_item.setter
    def root_item(self, value: Item | None) -> None:
        self.__root_item = value

    def __str__(self) -> str:
        return self.__to_str_recursive(self.root_item)

    def __to_str_recursive(self, item: Item | None, level: int = 0) -> str:
        if item is None:
            return "<None>"

        result = f"{'  ' * level}- {item.name}{NEW_LINE_CHAR}"
        for child in item.children:
            result += self.__to_str_recursive(child, level + 1)

        return result

    def __has_items(self, item: dict) -> bool:
        return Item.ITEMS_FIELD in item and item[Item.ITEMS_FIELD] is not None

    def __load_items(self, items: list[dict], parent: Item) -> None:
        for item in items:
            new_item = Item(
                item.get(Item.NAME_FIELD, ""),
                parent=parent,
                href=item.get(Item.HREF_FIELD),
                root_dir=self.__root_dir,
            )

            if self.__has_items(item):
                self.__load_items(item[Item.ITEMS_FIELD], new_item)

    def load(self, data: dict) -> None:
        self.root_item = Item(
            data.get(Item.NAME_FIELD, ""),
            href=data.get(Item.HREF_FIELD),
            root_dir=self.__root_dir,
        )
        if self.__has_items(data):
            self.__load_items(data[Item.ITEMS_FIELD], self.root_item)

    def merge(self, other: "TableOfContent") -> "TableOfContent":
        if self.root_item is None:
            self.root_item = other.root_item
        elif other.root_item is not None:
            self.root_item.add_child(other.root_item)
        else:
            logger.warning("Both TableOfContent are empty. Nothing to merge.")

        return self
