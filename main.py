from functools import wraps
import os
from typing import Annotated
import typer

from mindmap.models import TableOfContent
from mindmap.utils import load_indexes, read_yml_file, write_md_file
from rich.console import Console

OUTPUT_DIR = "output"
META_HEADER = """---
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
  initialExpandLevel: 3
---"""

app = typer.Typer()
console = Console()


def before_after_command(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        console.print("🚀 Starting...")
        try:
            result = f(*args, **kwargs)
            console.print("✅ Done")
            return result
        except Exception as e:
            console.print_exception(e)
            console.print("❌ Failed")

    return decorated


@app.command("well-architected")
def generate_azure_well_architect_mind_map():
    console.print("🗺️ Generating Mindmap for Azure Well-Architected..."
                  )
    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, "well-architected")
    toc_files = load_indexes(doc_dir)

    console.print(f"Total {len(toc_files)} mind maps will be generated")

    for idx, x in enumerate(toc_files):
        dir_path, file_path = x
        content = read_yml_file(file_path)

        console.print(f"Processing {file_path}...")

        toc = TableOfContent(
            root_dir=dir_path,
            root_uri="https://learn.microsoft.com/en-us/azure/well-architected/",
        )
        toc.convert_from_dict(content[0])

        result = toc.to_mindmap()

        output_dir = os.path.join(cwd_dir, OUTPUT_DIR)
        readme_file = os.path.join(output_dir, f"well-architected-mindmap-{idx+1}.md")
        write_md_file(result, readme_file, META_HEADER)

        console.print(f"Generated {readme_file}")


@app.command("list")
@before_after_command
def list_toc_files(path: Annotated[str, typer.Argument()]):
    console.print(f"📂 Listing all TOC files in {path}...")

    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, path)
    toc_files = load_indexes(doc_dir)

    console.print(f"Total {len(toc_files)} files found")

    toc_files.sort(key=lambda x: x[1])
    for idx, x in enumerate(toc_files):
        _, file_path = x
        console.print(f"{idx+1}. {file_path}")


@app.command("docs")
def generate_azure_docs_mindmap():
    console.print("🗺️ Generating Mindmap for Azure Docs...")

    cwd_dir = os.getcwd()
    doc_dir = os.path.join(cwd_dir, "azure-docs")
    toc_folders = load_indexes(doc_dir)

    console.print(f"Total {len(toc_folders)} mind maps will be generated")

    toc_folders.sort(key=lambda x: x[1])

    for idx, x in enumerate(toc_folders):
        dir_path, file_path = x
        content = read_yml_file(file_path)

        console.print(f"Processing {file_path}...")

        toc = TableOfContent(root_dir=dir_path, root_uri="https://docs.microsoft.com/en-us/azure/")

        toc.convert_from_dict(content[0])

        result = toc.to_mindmap()

        output_dir = os.path.join(cwd_dir, OUTPUT_DIR)
        readme_file = os.path.join(output_dir, f"docs-{idx+1}.md")
        write_md_file(result, readme_file, META_HEADER)

        console.print(f"Generated {readme_file}")


if __name__ == "__main__":
    app()
