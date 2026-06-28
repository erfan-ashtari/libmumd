<div align="center">

# libmumd

**Convert documents to Markdown with ease.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/erfan-ashtari/libmumd)](https://github.com/erfan-ashtari/libmumd/releases)

</div>

---

## Features

- **PDF to Markdown** — High-quality conversion using PyMuPDF
- **Office to Markdown** — Convert `.docx`, `.pptx`, `.xlsx`, and more
- **CLI & Library** — Use as a command-line tool or import in your Python code
- **Cross-platform** — Works on Windows, macOS, and Linux
- **Fallback support** — Uses `markitdown` when LibreOffice is unavailable

## Installation

```bash
pip install git+https://github.com/erfan-ashtari/libmumd.git
```

Or install from source:

```bash
git clone https://github.com/erfan-ashtari/libmumd.git
cd libmumd
pip install .
```

## Quick Start

### Command Line

```bash
# Convert PDF to Markdown
libmumd document.pdf

# Specify output file
libmumd document.docx output.md
```

### Python

```python
from libmumd import convert_file

# Basic usage
result = convert_file("report.pdf")
print(result)  # {'status': 'ok', 'chars': 1234, 'output': 'report.md'}

# Custom output path
result = convert_file("presentation.pptx", "slides.md")
```

## Supported Formats

| Format | Extension | Method |
|--------|-----------|--------|
| PDF | `.pdf` | PyMuPDF |
| Word | `.docx`, `.doc` | LibreOffice |
| PowerPoint | `.pptx`, `.ppt` | LibreOffice |
| Excel | `.xlsx`, `.xls` | LibreOffice |
| OpenDocument | `.odt`, `.odp`, `.ods` | LibreOffice |
| Rich Text | `.rtf` | LibreOffice |
| Other | * | markitdown |

## Requirements

### Python Packages (Auto-installed)

- `pymupdf4llm` — PDF conversion
- `markitdown` — Fallback converter

### LibreOffice (Manual Install)

LibreOffice is required for Office document conversion.

| OS | Command |
|----|---------|
| **Windows** | `winget install --id TheDocumentFoundation.LibreOffice` |
| **macOS** | `brew install --cask libreoffice` |
| **Linux** | `sudo apt-get install libreoffice` |

Or download manually from [libreoffice.org](https://www.libreoffice.org/).

> **Note:** The package will attempt to auto-install LibreOffice if missing, but manual installation is recommended.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF processing
- [markitdown](https://github.com/microsoft/markitdown) — Document conversion
- [LibreOffice](https://www.libreoffice.org/) — Office document handling
