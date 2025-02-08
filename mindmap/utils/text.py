INDENT_SIZE = 2


def remove_chars(s: str) -> str:
    chars_to_remove = "'?():"
    table = str.maketrans("", "", chars_to_remove)
    return s.translate(table)


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
