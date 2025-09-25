import logging
import os
from io import StringIO

from mindmap.models import Item, TableOfContent
from mindmap.utils.file import NEW_LINE_CHAR, read_md_file
from mindmap.utils.text import (
    INDENT_SIZE,
    fill_with_hash,
    fill_with_space,
    format_to_markdown_link,
)

logger = logging.getLogger(__name__)

MAX_HEADER_LEVEL = 6


class MindMapConverter:
    __root_dir: str
    __root_uri: str

    def __init__(self, root_dir: str = "/", root_uri: str = "/"):
        self.__root_dir = root_dir
        self.__root_uri = root_uri

    @property
    def root_dir(self) -> str:
        return self.__root_dir

    @root_dir.setter
    def root_dir(self, value: str) -> None:
        if value is None:
            raise ValueError("Root directory cannot be None.")

        self.__root_dir = value

    @property
    def root_uri(self) -> str:
        return self.__root_uri

    @root_uri.setter
    def root_uri(self, value: str) -> None:
        if value is None:
            raise ValueError("Root URI cannot be None.")

        self.__root_uri = value

    def __is_external_or_non_markdown_href(self, item: Item) -> bool:
        return (
            not item.href
            or item.href.startswith(("http://", "https://"))
            or item.href.endswith((".yml", ".yaml"))
        )

    def __write_header_line(self, item: Item, text: StringIO, level: int) -> None:
        # Item's name starts with '#' means it is a header
        line_text = (
            item.name
            if isinstance(item.name, str) and item.name.startswith("#")
            else f" {item.name}"
        )

        text.write(f"{fill_with_hash(level + 1)}{line_text}{NEW_LINE_CHAR}")
        text.write(NEW_LINE_CHAR)

    def __is_markdown_href(self, item: Item) -> bool:
        return (
            item.href is not None
            and not item.href.startswith(("http://", "https://"))
            and item.href.endswith(".md")
        )

    def __write_markdown(
        self, item: Item, text: StringIO, level: int, max_level: int
    ) -> None:
        root_dir = item.root_dir if item.root_dir is not None else self.root_dir

        md_file = os.path.join(root_dir, item.href)

        try:
            markdown_content = read_md_file(md_file)
        except FileNotFoundError:
            logger.warning(f"Markdown file {md_file} not found, skip it.")
            return

        if markdown_content is None:
            logger.warning(f"Markdown file {md_file} is empty, skip it.")
            return

        for header in markdown_content.headers:
            local_level = header.count("#")
            total_level = level + local_level

            if max_level >= 0 and total_level >= max_level:
                continue

            link_text = format_to_markdown_link(
                self.root_uri, item.href, header, local_level
            )

            if total_level > MAX_HEADER_LEVEL:
                text.write(
                    f"{fill_with_space(total_level - MAX_HEADER_LEVEL - 1, INDENT_SIZE)}-{link_text}{NEW_LINE_CHAR}"
                )
                text.write(NEW_LINE_CHAR)
            else:
                text.write(f"{fill_with_hash(total_level)}{link_text}{NEW_LINE_CHAR}")
                text.write(NEW_LINE_CHAR)

    def __to_mindmap_recursive(
        self, item: Item, text: StringIO, level: int, max_level: int
    ) -> StringIO:
        """
        Recursively converts an Item and its children to a mindmap representation.

        Args:
            item (Item): The current item to convert.
            text (StringIO): The StringIO object to write the mindmap content.
            level (int): The current depth level in the mindmap.
            max_level (int): The maximum depth level to convert; -1 means no limit.

        Returns:
            StringIO: The StringIO object containing the mindmap content.
        """
        # Only convert the level less than the max level
        if max_level >= 0 and level >= max_level:
            return text

        if self.__is_external_or_non_markdown_href(item):
            self.__write_header_line(item, text, level)

        elif self.__is_markdown_href(item):
            self.__write_markdown(item, text, level, max_level)

        if item.children:
            for _, child in enumerate(item.children):
                self.__to_mindmap_recursive(child, text, level + 1, max_level)

        return text

    def convert(self, toc: TableOfContent, max_level: int = -1) -> str:
        """
        Convert the table of content to a mindmap.

        Args:
            toc (TableOfContent): The table of content to convert.
            max_level (int): The maximum level to convert to the mindmap, -1 means all levels.

        Returns:
            str: The converted mindmap as a string.
        """
        logger.debug("Start converting table of content to mindmap.")
        text = StringIO()
        if toc.root_item is None:
            raise ValueError("Table of content is empty.")

        content = self.__to_mindmap_recursive(toc.root_item, text, 0, max_level)
        # Remove the last newline
        result = content.getvalue()[::-1].replace(NEW_LINE_CHAR, "", 1)[::-1]

        logger.debug("Finish converting table of content to mindmap.")
        return result
