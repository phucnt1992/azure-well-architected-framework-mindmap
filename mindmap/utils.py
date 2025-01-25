import os
from io import StringIO

import yaml

from mindmap.models import Item, TableOfContent


def remove_chars(s: str) -> str:
    chars_to_remove = "'?():"
    table = str.maketrans("", "", chars_to_remove)
    return s.translate(table)


def load_indexes(path: str, file_name: str = "toc.yml", exclude_dir: str = None) -> list[str]:
    """Load all files in the given path and file name."""
    index_files = []
    for dir_path, _, files in os.walk(path):
        for file in files:
            if file.lower() == file_name and (exclude_dir is None or exclude_dir not in dir_path):
                index_files.append((dir_path, os.path.join(dir_path, file)))

    return index_files


def read_yml_file(index_file: str) -> dict:
    """Read the index.yml file and return the content."""
    with open(index_file, "r") as file:
        # Remove found character '\t' that cannot start any token
        file_content = file.read().replace("\t", "")
        return yaml.safe_load(file_content)


def read_md_file(md_file: str) -> list[str]:
    """Read the markdown file and return the content."""
    with open(md_file, "r") as file:
        lines = file.readlines()

    headers = filter(lambda line: line.startswith("#") and "customer intent:" not in line.lower(), lines)

    return list(
        map(lambda line: line.replace(TableOfContent.NEW_LINE_CHAR, ""), headers)
    )


def write_md_file(content: str, file: str, meta: str = None) -> str:
    """Write the content to a markdown file."""
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, "w", encoding="utf-8") as output_file:
        if meta is not None:
            output_file.write(meta)
            output_file.write("\n\n")
        output_file.write(content)


def format_to_markdown_link(uri: str, href: str, header: str, level: int) -> str:
    stripped_header = header.lstrip("#").strip()
    header_id = (
        f"#{remove_chars(stripped_header.lower().replace(' ', '-'))}"
        if level > 1
        else ""
    )

    return f" [{stripped_header}]({uri}{href.removesuffix('.md')}{header_id})"


def fill_with_hash(length: int) -> str:
    return "#" * length


def fill_with_space(length: int, indent_size: int) -> str:
    return " " * length * indent_size


class MindmapConverter:
    INDENT_SIZE = 2
    table_of_content: "TableOfContent"
    root_dir: str
    root_uri: str

    def __init__(self, table_of_content: dict, root_dir: str, root_uri: str = "/"):
        self.table_of_content = table_of_content
        self.root_dir = root_dir
        self.root_uri = root_uri

    def __is_non_markdown_href(self, item: Item) -> bool:
        return item.href is None \
            or item.href.startswith("http") \
            or item.href.endswith(".yml") \
            or item.href.endswith(".yaml")

    def __write_non_markdown(self, item: Item, text: StringIO, level: int) -> None:
        # Item's name starts with '#' means it is a header
        line_text = item.name \
            if item.name is str and item.name.startswith("#") \
            else f" {item.name}"

        text.write(f"{fill_with_hash(level + 1)}{line_text}{self.NEW_LINE_CHAR}")
        text.write(self.NEW_LINEd_CHAR)

    def __is_markdown_href(self, item: Item) -> bool:
        return item.href is not None \
            and not item.href.startswith("http") \
            and item.href.endswith(".md")

    def __write_markdown(self, item: Item, text: StringIO, level: int, max_level: int) -> None:
        root_dir = item.root_dir if item.root_dir is not None else self.__root_dir
        md_file = os.path.join(root_dir, item.href)

        try:
            headers = read_md_file(md_file)
        except FileNotFoundError:
            headers = []

        for header in headers:
            local_level = header.count("#")
            total_level = level + local_level

            if max_level >= 0 and total_level >= max_level:
                continue

            link_text = format_to_markdown_link(self.root_dir, item.href, header, local_level)

            if total_level > self.MAX_HEADER_LEVEL:
                text.write(f"{fill_with_space(total_level - self.MAX_HEADER_LEVEL - 1, self.INDENT_SIZE)}-{link_text}{self.NEW_LINE_CHAR}")
                text.write(self.NEW_LINE_CHAR)
            else:
                text.write(f"{fill_with_hash(total_level)}{link_text}{self.NEW_LINE_CHAR}")
                text.write(self.NEW_LINE_CHAR)

    def __to_mindmap_recursive(self, item: dict, text: StringIO, level: int, max_level: int) -> StringIO:
        # Only convert the level less than the max level
        if max_level >= 0 and level >= max_level:
            return text

        if self.__is_non_markdown_href(item):
            self.__write_non_markdown(item, text, level)

        if self.__is_markdown_href(item):
            self.__write_markdown(item, text, level, max_level)

        for child in item.children:
            self.__to_mindmap_recursive(child, text, level + 1, max_level)

        return text

    def to_mindmap(self, max_level: int = -1) -> str:
        """Convert the table of content to a mindmap.
        max_level: The maximum level to convert to the mindmap, -1 means all levels.
        """
        with StringIO() as text:
            result = self.__to_mindmap_recursive(self.root_item, text, 0, max_level)
            # Remove the last newline
            return result.getvalue()[::-1].replace(self.NEW_LINE_CHAR, "", 1)[::-1]
