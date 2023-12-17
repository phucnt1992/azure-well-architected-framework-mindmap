# Azure Well-Architected Framework Mindmap

[![CI pipeline](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/ci.yml/badge.svg)](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/ci.yml)
[![CD pipeline](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/cd.yml/badge.svg)](https://github.com/phucnt1992/azure-well-architected-framework-mindmap/actions/workflows/cd.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=coverage)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=bugs)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=phucnt1992_azure-well-architected-framework-mindmap&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)

[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=phucnt1992_azure-well-architected-framework-mindmap)](https://sonarcloud.io/summary/new_code?id=phucnt1992_azure-well-architected-framework-mindmap)

This is a mindmap generator of the [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/).

Published page: 🗺️ [Mind map](https://phucnt1992.github.io/azure-well-architected-framework-mindmap/)

![Azure Well-Architected Framework Mind map](docs/image.png)

## Requirements

- [Python 3.12](https://www.python.org/downloads/)
- [NodeJS LTS](https://nodejs.org/)
- [Taskfile](https://taskfile.dev/)

## Usage

```bash
# Install dependencies
task init

# Run tests
task test

# Generate the mindmap (in the `output` folder)
# 1. Clone docs from the official repo
task clone-docs
# 2. Markdown format only
task run
# 3. HTML format
task generate

# Clean all workspace
task clean
```

## License

![GitHub License](https://img.shields.io/github/license/phucnt1992/azure-well-architected-framework-mindmap)

This project is licensed under the [MIT License](LICENSE).
