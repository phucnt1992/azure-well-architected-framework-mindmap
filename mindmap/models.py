import os
from ctypes import Array
from io import StringIO


def read_md_file(md_file: str) -> Array[str]:
    """Read the markdown file and return the content."""
    with open(md_file, "r") as file:
        lines = file.readlines()

    headers = filter(lambda line: line.startswith("#"), lines)

    return list(
        map(lambda line: line.replace(TableOfContent.NEW_LINE_CHAR, ""), headers)
    )


class Item:
    NAME_FIELD = "name"
    HREF_FIELD = "href"
    ITEMS_FIELD = "items"

    name: str
    parent: "Item"
    children: Array["Item"]
    href: str

    def __init__(
        self,
        name: str,
        parent: "Item" = None,
        href: str = None,
    ):
        self.name = name
        self.href = href
        self.children = []

        if parent is not None:
            self.parent = parent
            self.parent.add_child(self)

    def add_child(self, child: "Item"):
        self.children.append(child)


class TableOfContent:
    MAX_HEADER_LEVEL = 6
    INDENT_SIZE = 2
    NEW_LINE_CHAR = "\n"

    __root: Item
    __root_dir: str
    __root_uri: str

    def __init__(self, root: Item = None, root_dir: str = None, root_uri: str = "/"):
        self.__root = root
        self.__root_dir = root_dir
        self.__root_uri = root_uri

    def __str__(self) -> str:
        return self.__str_recursive(self.__root)

    def __str_recursive(self, item: Item, level: int = 0) -> str:
        result = f"{'  ' * level}- {item.name}{self.NEW_LINE_CHAR}"
        for child in item.children:
            result += self.__str_recursive(child, level + 1)

        return result

    def convert_from_dict(self, data: dict) -> None:
        self.__root = Item(data[Item.NAME_FIELD], href=data.get(Item.HREF_FIELD, None))
        self.__convert_items(data[Item.ITEMS_FIELD], self.__root)

    def __convert_items(self, items: Array[dict], parent: Item) -> None:
        for item in items:
            new_item = Item(
                item.get(Item.NAME_FIELD),
                parent=parent,
                href=item.get(Item.HREF_FIELD, None),
            )

            if Item.ITEMS_FIELD in item:
                self.__convert_items(item[Item.ITEMS_FIELD], new_item)

    def to_mindmap(self, root_level: int = 0) -> str:
        with StringIO() as text:
            result = self.__to_mindmap_recursive(self.__root, text, root_level)
            # Remove the last newline
            return result.getvalue()[::-1].replace(self.NEW_LINE_CHAR, "", 1)[::-1]

    def __to_mindmap_recursive(self, item: Item, text: StringIO, level: int = 0) -> str:
        if (
            item.href is None
            or item.href.endswith(".yml")
            or item.href.endswith(".yaml")
        ):
            lint_name = item.name if item.name.startswith("#") else f" {item.name}"
            text.write(
                f"{self.__fill_with_hash(level + 1)}{lint_name}{self.NEW_LINE_CHAR}"
            )
            text.write(self.NEW_LINE_CHAR)

        if item.href is not None and item.href.endswith(".md"):
            md_file = os.path.join(self.__root_dir, item.href)
            headers = read_md_file(md_file)
            for header in headers:
                local_level = header.count("#")
                total_level = level + local_level
                link_text = self.__format_to_md_link(item.href, header, local_level)

                # Maximum Header Level is 6 in Markdown
                if total_level > self.MAX_HEADER_LEVEL:
                    text.write(
                        f"{self.__fill_with_space(total_level - self.MAX_HEADER_LEVEL - 1)}-{link_text}{self.NEW_LINE_CHAR}"
                    )
                    text.write(self.NEW_LINE_CHAR)

                else:
                    text.write(
                        f"{self.__fill_with_hash(total_level)}{link_text}{self.NEW_LINE_CHAR}"
                    )
                    text.write(self.NEW_LINE_CHAR)

        for child in item.children:
            self.__to_mindmap_recursive(child, text, level + 1)

        return text

    def __fill_with_hash(self, length: int) -> str:
        return "#" * length

    def __fill_with_space(self, length: int) -> str:
        return " " * length * self.INDENT_SIZE

    def __format_to_md_link(self, href: str, header: str, level: int) -> str:
        stripped_header = header.lstrip("#").strip()
        header_id = f"#{stripped_header.lower().replace(' ', '-')}" if level > 1 else ""

        return f" [{stripped_header}]({self.__root_uri}{href.removesuffix('.md')}{header_id})"
