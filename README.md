# libmumd

Convert documents (Office, PDF) to Markdown.

## Installation

```bash
pip install .
```

## Usage

### As a library

```python
from libmumd import convert_file

result = convert_file("document.pdf")
# or
result = convert_file("document.docx", "output.md")
```

### As a CLI

```bash
libmumd document.pdf
libmumd document.docx output.md
```

## Requirements

### Python packages (installed automatically)

- pymupdf4llm
- markitdown

### LibreOffice (required for Office file conversion)

LibreOffice is not a Python package, so pip cannot install it. You must install it manually:

**Windows:**
```bash
winget install --id TheDocumentFoundation.LibreOffice
```
Or download from https://www.libreoffice.org/

**Mac:**
```bash
brew install --cask libreoffice
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libreoffice
```

The package will try to auto-install LibreOffice if it's missing, but manual installation is recommended.
