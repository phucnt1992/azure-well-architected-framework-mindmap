import os

import yaml

NEW_LINE_CHAR = "\n"


def scan_toc_files(
    path: str, file_name: str = "toc.yml", exclude_dir: str = None
) -> list[str]:
    """Load all files in the given path and file name."""
    index_files = []
    for dir_path, _, files in os.walk(path):
        for file in files:
            if file.lower() == file_name and (
                exclude_dir is None or exclude_dir not in dir_path
            ):
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

    headers = filter(
        lambda line: line.startswith("#") and "customer intent:" not in line.lower(),
        lines,
    )

    return list(map(lambda line: line.replace(NEW_LINE_CHAR, ""), headers))


def write_md_file(content: str, file: str, meta: str = None) -> str:
    """Write the content to a markdown file."""
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, "w", encoding="utf-8") as output_file:
        if meta is not None:
            output_file.write(meta)
            output_file.write("\n\n")
        output_file.write(content)
