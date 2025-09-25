import logging
import os
from dataclasses import dataclass
from typing import Optional

import yaml

logger = logging.getLogger(__name__)

NEW_LINE_CHAR = "\n"
CHUNK_SIZE = 1024 * 1024  # 1MB


@dataclass
class MarkdownContent:
    title: str
    description: str | None
    headers: list[str]

    def __init__(
        self,
        title: str = "",
        description: str | None = None,
        headers: list[str] | None = None,
    ):
        self.title = title
        self.description = description
        self.headers = headers if headers else []


def scan_toc_files(
    path: str, file_name: str = "toc.yml", exclude_dir: Optional[str] = None
) -> list[tuple[str, str]]:
    """
    Load all files in the given path with the specified file name.

    Args:
        path (str): The root directory to scan.
        file_name (str): The name of the files to look for. Default is "toc.yml".
        exclude_dir (Optional[str]): A directory name to exclude from the scan.
    """
    index_files = []
    for dir_path, _, files in os.walk(path):
        for file in files:
            if file.lower() == file_name and (
                not exclude_dir or exclude_dir not in dir_path.split(os.sep)
            ):
                index_files.append((dir_path, os.path.join(dir_path, file)))

    return index_files


def read_yml_file(index_file: str) -> dict:
    """Read the YAML file specified by `index_file` and return the content."""
    with open(index_file, "r", encoding="utf-8") as file:
        # Remove leading tab characters from each line to avoid breaking YAML indentation
        file_content = file.read().replace("\t", "")
        return yaml.safe_load(file_content)


def __parse_front_matter(lines: list[str]) -> tuple[str, Optional[str], int]:
    """Return (title, description, content_start_idx) parsed from lines."""
    title: str = ""
    description: Optional[str] = None
    content_start_idx: int = 0

    if lines and lines[0].startswith("---"):
        for idx, line in enumerate(lines[1:], start=1):
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                description = line.partition(":")[2].strip()
            elif line.startswith("---"):
                content_start_idx = idx + 1
                break
    else:
        for idx, line in enumerate(lines):
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                content_start_idx = idx
                break

    return title, description, content_start_idx


def __collect_headers(lines: list[str], start_idx: int) -> list[str]:
    """Collect header lines from lines starting at start_idx, filtering unwanted ones."""
    headers: list[str] = []
    for line in lines[start_idx:]:
        if not line.startswith("#"):
            continue
        if "#customer intent:" in line.lower():
            continue
        headers.append(line.replace(NEW_LINE_CHAR, ""))
    return headers


def read_md_file(md_file: str) -> Optional["MarkdownContent"]:
    """Read the markdown file and return the content."""
    try:
        with open(md_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        title, description, content_start_idx = __parse_front_matter(lines)
        headers = __collect_headers(lines, content_start_idx)

        # Ensure title is not empty
        if not title and headers:
            title = headers[0].lstrip("#").strip()

        return MarkdownContent(title, description, headers)
    except FileNotFoundError:
        logger.warning(f"File {md_file} not found.")
        return None


def write_md_file(content: str, file: str, meta: Optional[str] = None) -> None:
    """
    Write the content to a markdown file.

    If `file` is a filename in the current directory (no directory part), no directory is created.
    If `file` is a relative path like "./file.md", the directory part is ".", which is safe to pass to os.makedirs.
    For very large files, consider writing in chunks.
    """
    dir_name = os.path.dirname(file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(file, "w", encoding="utf-8") as output_file:
        if meta is not None:
            output_file.write(meta)
            output_file.write("\n\n")

        # For large files, write in chunks
        for i in range(0, len(content), CHUNK_SIZE):
            end = min(i + CHUNK_SIZE, len(content))
            output_file.write(content[i:end])
