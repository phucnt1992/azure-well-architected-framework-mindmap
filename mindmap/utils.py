import os

import yaml


def load_indexes(path: str, file_name: str = "toc.yml") -> list[str]:
    """Load all files in the given path and file name."""
    index_files = []
    for dir_path, _, files in os.walk(path):
        for file in files:
            if file.lower() == file_name:
                index_files.append((dir_path, os.path.join(dir_path, file)))

    return index_files


def read_yml_file(index_file: str) -> dict:
    """Read the index.yml file and return the content."""
    with open(index_file, "r") as file:
        return yaml.safe_load(file)


def write_md_file(content: str, file: str, meta: str = None) -> str:
    """Write the content to a markdown file."""
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, "w", encoding="utf-8") as output_file:
        if meta is not None:
            output_file.write(meta)
            output_file.write("\n\n")
        output_file.write(content)
