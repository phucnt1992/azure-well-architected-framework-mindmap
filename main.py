import os

from mindmap.models import TableOfContent
from mindmap.utils import load_indexes, read_yml_file, write_md_file

SCAN_DIR = "well-architected"
OUTPUT_DIR = "output"
META_HEADER = """---
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
  initialExpandLevel: 3
---"""

if __name__ == "__main__":
    cwd_dir = os.getcwd()

    doc_dir = os.path.join(cwd_dir, SCAN_DIR)

    toc_files = load_indexes(doc_dir, "TOC.yml")

    for idx, x in enumerate(toc_files):
        dir_path, file_path = x
        content = read_yml_file(file_path)

        toc = TableOfContent(
            root_dir=dir_path,
            root_uri="https://learn.microsoft.com/en-us/azure/well-architected/",
        )
        toc.convert_from_dict(content[0])

        result = toc.to_mindmap()

        output_dir = os.path.join(cwd_dir, OUTPUT_DIR)
        readme_file = os.path.join(output_dir, f"MINDMAP-{idx+1}.md")
        write_md_file(result, readme_file, META_HEADER)
