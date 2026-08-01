#!/usr/bin/env python3
import argparse
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from convert import convert_to_epub
from mailer import send_to_kindle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert documents to EPUB and email them to your Kindle."
    )
    parser.add_argument("files", nargs="+", help="Files to convert and send")
    args = parser.parse_args()

    failed = False
    for file_arg in args.files:
        src = Path(file_arg)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                epub_path = convert_to_epub(src, Path(tmp))
                send_to_kindle(epub_path)
            print(f"OK: {src}")
        except Exception as e:
            print(f"FAILED: {src}: {e}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
