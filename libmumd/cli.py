import sys
from .convert import convert_file


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("Usage: libmumd <input_file> [output_file]")
        print("\nConvert documents (Office, PDF) to Markdown.")
        print("\nExamples:")
        print("  libmumd document.pdf")
        print("  libmumd document.docx output.md")
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = convert_file(input_file, output_file)
        print(f"OK:{result.get('chars', 'fallback')}")
    except Exception as e:
        print(f"FAIL:{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
