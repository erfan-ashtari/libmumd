import subprocess
import shutil
import tempfile
import platform
from pathlib import Path

OFFICE_EXTS = {'.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.odt', '.odp', '.ods', '.rtf'}
PDF_EXT = '.pdf'


def find_soffice():
    path = shutil.which('soffice')
    if path:
        return path
    system = platform.system()
    if system == 'Windows':
        candidates = [
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
        ]
        for c in candidates:
            if Path(c).exists():
                return c
    elif system == 'Darwin':
        candidate = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        if Path(candidate).exists():
            return candidate
    return None


def install_soffice():
    system = platform.system()
    try:
        if system == 'Windows':
            subprocess.run(['winget', 'install', '--id', 'TheDocumentFoundation.LibreOffice', '--accept-package-agreements', '--accept-source-agreements'], check=True)
        elif system == 'Darwin':
            subprocess.run(['brew', 'install', '--cask', 'libreoffice'], check=True)
        elif system == 'Linux':
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libreoffice'], check=True)
        else:
            return None
        return find_soffice()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def convert_office_to_pdf(office_file, tmp_dir):
    soffice = find_soffice() or install_soffice()
    if not soffice:
        raise RuntimeError("LibreOffice is not installed and could not be auto-installed")
    expected_pdf = tmp_dir / (office_file.stem + '.pdf')
    cmd = [soffice, '--headless', '--convert-to', 'pdf', '--outdir', str(tmp_dir), str(office_file)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if expected_pdf.exists():
        return expected_pdf
    err = result.stderr.strip()[:200] if result.stderr else 'unknown error'
    raise RuntimeError(f"LibreOffice failed: {err}")


def convert_with_markitdown(input_file, output_file):
    result = subprocess.run(
        ['markitdown', str(input_file), '-o', str(output_file)],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[:200] or f"markitdown exit code {result.returncode}")


def convert_file(input_file, output_file=None):
    try:
        import pymupdf4llm
    except ImportError:
        raise ImportError("pymupdf4llm not installed. Run: pip install pymupdf4llm")

    input_path = Path(input_file).resolve()
    if output_file is None:
        output_path = input_path.with_suffix('.md')
    else:
        output_path = Path(output_file).resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"File not found: {input_path}")

    ext = input_path.suffix.lower()

    if ext == PDF_EXT:
        md_text = pymupdf4llm.to_markdown(str(input_path))
        output_path.write_text(md_text, encoding='utf-8')
        return {"status": "ok", "chars": len(md_text), "output": str(output_path)}

    elif ext in OFFICE_EXTS:
        tmp_dir = Path(tempfile.mkdtemp(prefix="office2md_"))
        try:
            pdf_file = convert_office_to_pdf(input_path, tmp_dir)
            md_text = pymupdf4llm.to_markdown(str(pdf_file))
            output_path.write_text(md_text, encoding='utf-8')
            return {"status": "ok", "chars": len(md_text), "output": str(output_path)}
        except Exception as e:
            try:
                convert_with_markitdown(input_path, output_path)
                return {"status": "ok", "method": "markitdown", "output": str(output_path)}
            except Exception as e2:
                raise RuntimeError(f"{e} (markitdown fallback: {e2})")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    else:
        try:
            convert_with_markitdown(input_path, output_path)
            return {"status": "ok", "method": "markitdown", "output": str(output_path)}
        except Exception as e:
            raise RuntimeError(f"Unsupported extension {ext}: {e}")


def convert(input_file, output_file=None):
    return convert_file(input_file, output_file)
