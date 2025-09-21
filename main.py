import logging
import os
from typing import Annotated, Optional

import typer
from rich.logging import RichHandler

from mindmap.converters import MindMapConverter
from mindmap.models import Item, TableOfContent
from mindmap.utils.file import read_yml_file, scan_toc_files, write_md_file

OUTPUT_DIR = "output"
DOC_DIR = ".tmp"

META_HEADER = """---
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
  initialExpandLevel: 3
---"""

app = typer.Typer()
logger_FORMAT = "%(message)s"
logger_DEFAULT_LEVEL = logging.INFO

logger = logging.getLogger(__name__)


@app.callback()
def main(
    verbose: Annotated[
        Optional[bool], typer.Option("--verbose", "-v", help="Enable verbose logs")
    ] = False,
):
    logger_level = logger_DEFAULT_LEVEL
    if verbose:
        logger_level = logging.DEBUG

    logging.basicConfig(
        level=logger_level,
        format=logger_FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
    )

    if verbose:
        logger.debug("Verbose mode is enabled")


@app.command("well-architected")
def generate_azure_well_architect_mind_map():
    logger.info("🗺️ Generating Mindmap for Azure Well-Architected...")
    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, DOC_DIR, "well-architected")
    toc_files = scan_toc_files(doc_dir, exclude_dir="bread")
    converter = MindMapConverter(
        root_dir=doc_dir,
        root_uri="https://learn.microsoft.com/en-us/azure/well-architected/",
    )

    logger.info(f"Total {len(toc_files)} mind maps will be generated")

    for idx, x in enumerate(toc_files):
        dir_path, file_path = x
        content = read_yml_file(file_path)

        logger.info(f"Processing {file_path}...")

        toc = TableOfContent(root_dir=dir_path)
        toc.load(content[0])

        result = converter.convert(toc)

        output_dir = os.path.join(cwd_dir, OUTPUT_DIR)
        readme_file = os.path.join(output_dir, f"well-architected-mindmap-{idx+1}.md")
        write_md_file(result, readme_file, META_HEADER)

        logger.info(f"Generated {readme_file}")


@app.command("list")
def list_toc_files(path: Annotated[str, typer.Argument()]):
    logger.info(f"📂 Listing all TOC files in {path}...")

    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, path)
    toc_files = scan_toc_files(doc_dir)

    logger.info(f"Total {len(toc_files)} files found")

    toc_files.sort(key=lambda x: x[1])
    for idx, x in enumerate(toc_files):
        _, file_path = x
        logger.info(f"{idx+1}. {file_path}")


@app.command("docs")
def generate_azure_docs_mindmap():
    logger.info("🗺️ Generating Mindmap for Azure Docs...")

    root_uri = "https://docs.microsoft.com/en-us/azure/"
    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, DOC_DIR, "azure-docs")
    output_dir = os.path.join(cwd_dir, OUTPUT_DIR)
    article_dir = os.path.join(doc_dir, "articles")
    toc_folders = scan_toc_files(doc_dir, exclude_dir="bread")

    logger.info(f"Total {len(toc_folders)} mind maps will be generated")

    converter = MindMapConverter(root_dir=doc_dir, root_uri=root_uri)
    toc = TableOfContent(
        root=Item(name="Azure Docs", href=root_uri),
        root_dir=doc_dir,
    )

    # Sort the files by name
    toc_folders.sort(key=lambda x: x[1])

    for _, toc_item in enumerate(toc_folders):
        dir_path, file_path = toc_item

        logger.info(f"Processing {file_path}...")

        articles = read_yml_file(file_path)
        article_path = (
            os.path.relpath(file_path, start=article_dir)
            .lower()
            .removesuffix("toc.yml")
        )
        current_toc = TableOfContent(root_dir=dir_path)
        converter.root_uri = f"{root_uri}{article_path}"

        if isinstance(articles, dict):
            articles = articles.get(Item.ITEMS_FIELD, [])

        for article_item in articles:
            article_toc = TableOfContent(root_dir=dir_path)

            article_toc.load(article_item)
            current_toc.merge(article_toc)

        article_content = converter.convert(current_toc)

        if current_toc.root_item is None:
            logger.warning("Current TOC root item is None, skip generating file.")
            continue

        file_name = (
            current_toc.root_item.name.lower().replace(" ", "-").replace("/", "-")
        )
        readme_file = os.path.join(output_dir, f"docs-{file_name}.md")

        write_md_file(article_content, readme_file, META_HEADER)
        logger.info(f"Generated {readme_file}")

        toc.merge(current_toc)

    converter.root_uri = root_uri
    result = converter.convert(toc, max_level=2)
    readme_file = os.path.join(output_dir, "docs.md")
    write_md_file(result, readme_file, META_HEADER)

    logger.info(f"Generated {readme_file}")


if __name__ == "__main__":
    app()
