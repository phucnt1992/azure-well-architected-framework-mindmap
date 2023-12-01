# Azure Well-Architected Framework Mindmap

This is a mindmap generator of the [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/).

![Code coverage](https://img.shields.io/codecov/c/github/phucnt1992/azure-well-architected-framework-mindmap)
[![CI pipeline](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/ci.yml/badge.svg)](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/ci.yml)
[![CD pipeline](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/cd.yml/badge.svg)](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/cd.yml)

## Requirements

- [Python 3.12](https://www.python.org/downloads/)
- [NodeJS LTS](https://nodejs.org/)

## Usage

```bash
# Install dependencies
make init

# Run tests
make test

# Generate the mindmap (in the `output` folder)
# 1. Clone docs from the official repo
make clone-docs
# 2. Markdown format only
make run
# 3. HTML format
make generate

# Clean all workspace
make clean
```

## License

![GitHub License](https://img.shields.io/github/license/phucnt1992/azure-well-architected-framework-mindmap)

This project is licensed under the [MIT License](LICENSE).
