import subprocess
import sys
import shutil
import tempfile
import platform
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

try:
    import pymupdf4llm
except ImportError:
    sys.exit("pymupdf4llm not installed. Run: pip install -r requirements.txt")


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
    print("LibreOffice not found. Attempting install...", file=sys.stderr)
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
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Auto-install failed: {e}", file=sys.stderr)
        return None


SOFFICE = find_soffice() or install_soffice()


def convert_office_to_pdf(office_file, tmp_dir):
    if not SOFFICE:
        raise RuntimeError("LibreOffice is not installed and could not be auto-installed")
    expected_pdf = tmp_dir / (office_file.stem + '.pdf')
    cmd = [SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', str(tmp_dir), str(office_file)]
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input_file> [output_file]")
        sys.exit(1)

    input_file = Path(sys.argv[1]).resolve()
    output_file = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_file.with_suffix('.md')

    if not input_file.is_file():
        sys.exit(f"File not found: {input_file}")

    ext = input_file.suffix.lower()

    if ext == PDF_EXT:
        try:
            md_text = pymupdf4llm.to_markdown(str(input_file))
            output_file.write_text(md_text, encoding='utf-8')
            print(f"OK:{len(md_text)}")
        except Exception as e:
            sys.exit(f"FAIL:{e}")

    elif ext in OFFICE_EXTS:
        tmp_dir = Path(tempfile.mkdtemp(prefix="office2md_"))
        try:
            pdf_file = convert_office_to_pdf(input_file, tmp_dir)
            md_text = pymupdf4llm.to_markdown(str(pdf_file))
            output_file.write_text(md_text, encoding='utf-8')
            print(f"OK:{len(md_text)}")
        except Exception as e:
            try:
                convert_with_markitdown(input_file, output_file)
                print(f"OK:fallback_markitdown")
            except Exception as e2:
                sys.exit(f"FAIL:{e} (markitdown fallback: {e2})")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    else:
        try:
            convert_with_markitdown(input_file, output_file)
            print(f"OK:fallback_markitdown")
        except Exception as e:
            sys.exit(f"FAIL:Unsupported extension {ext}: {e}")


if __name__ == "__main__":
    main()
