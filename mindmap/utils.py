import os
from ctypes import Array
from functools import reduce

import yaml


def load_indexes(path: str, file_name: str = "toc.yml") -> Array[str]:
    """Load all index.yml files in the given path."""
    index_files = []
    for dir_path, _, files in os.walk(path):
        reduce(
            lambda acc, file: acc.append((dir_path, os.path.join(dir_path, file)))
            if file == file_name
            else acc,
            files,
            index_files,
        )

    return index_files


def read_yml_file(index_file: str) -> dict:
    """Read the index.yml file and return the content."""
    with open(index_file, "r") as file:
        return yaml.safe_load(file)


def write_md_file(content: str, file: str) -> str:
    """Write the content to a markdown file."""
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, "w", encoding="utf-8") as output_file:
        output_file.write(content)
