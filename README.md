<div align="center">

# libmumd

**Convert documents to clean, LLM-ready Markdown.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/erfan-ashtari/libmumd)](https://github.com/erfan-ashtari/libmumd/releases)

</div>

---

## Why libmumd?

Most document converters produce messy output — broken tables, lost formatting, garbled non-English text. **libmumd** is different:

- **Better than markitdown alone** — Uses PyMuPDF's layout engine for cleaner, more accurate conversion
- **Multi-language support** — Handles Arabic, Chinese, Japanese, Korean, and European languages correctly
- **Table detection** — Automatically converts complex tables to Markdown format
- **Figure & image handling** — Extracts and references images properly
- **Layout-aware** — Preserves reading order, headers, and document structure
- **No GPU required** — Runs on any machine with Python

## Features

| Feature | Description |
|---------|-------------|
| **PDF → Markdown** | High-quality extraction with layout preservation |
| **Office → Markdown** | Convert `.docx`, `.pptx`, `.xlsx`, and more via LibreOffice |
| **Smart table parsing** | Complex tables become clean Markdown tables |
| **Image extraction** | Embedded images are saved and referenced |
| **Header detection** | Font sizes map to `#` heading levels automatically |
| **Inline formatting** | Preserves **bold**, *italic*, and `code` |
| **Multi-column layouts** | Reconstructs natural reading order |
| **OCR fallback** | Handles scanned documents when text layer is missing |

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

# Convert Office document
libmumd report.docx output.md
```

### Python

```python
from libmumd import convert_file

# Basic usage
result = convert_file("document.pdf")
print(result)
# {'status': 'ok', 'chars': 4523, 'output': 'document.md'}

# Custom output path
result = convert_file("presentation.pptx", "slides.md")
```

## Supported Formats

| Format | Extensions | Conversion Method |
|--------|------------|-------------------|
| PDF | `.pdf` | PyMuPDF (native) |
| Word | `.docx`, `.doc` | LibreOffice |
| PowerPoint | `.pptx`, `.ppt` | LibreOffice |
| Excel | `.xlsx`, `.xls` | LibreOffice |
| OpenDocument | `.odt`, `.odp`, `.ods` | LibreOffice |
| Rich Text | `.rtf` | LibreOffice |
| Other | Any | markitdown fallback |

## Requirements

### Python Packages (Auto-installed)

- `pymupdf4llm` — PDF extraction engine
- `markitdown` — Fallback converter

### LibreOffice (Required for Office Files)

LibreOffice is needed to convert Word, PowerPoint, and Excel files.

| OS | Installation |
|----|--------------|
| **Windows** | `winget install --id TheDocumentFoundation.LibreOffice` |
| **macOS** | `brew install --cask libreoffice` |
| **Linux** | `sudo apt-get install libreoffice` |

Or download from [libreoffice.org](https://www.libreoffice.org/).

> **Note:** PDF conversion works without LibreOffice. Only Office document conversion requires it.

## Output Quality Comparison

| Aspect | markitdown only | libmumd |
|--------|-----------------|---------|
| Table formatting | Inconsistent | Clean Markdown tables |
| Multi-language | Basic | Full Unicode support |
| Layout preservation | None | Reading order preserved |
| Image handling | Limited | Extracted and referenced |
| Header detection | None | Automatic heading levels |

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

- [PyMuPDF4LLM](https://github.com/pymupdf/pymupdf4llm) — PDF extraction engine
- [markitdown](https://github.com/microsoft/markitdown) — Fallback converter
- [LibreOffice](https://www.libreoffice.org/) — Office document handling
