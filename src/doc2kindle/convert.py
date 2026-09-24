import shutil
import subprocess
from pathlib import Path

from .cover import generate_cover


def convert_to_epub(src: Path, dest_dir: Path) -> Path:
    if shutil.which("ebook-convert") is None:
        raise RuntimeError(
            "ebook-convert not found on $PATH — install Calibre:\n"
            "  Linux: sudo apt install calibre\n"
            "  macOS: brew install --cask calibre && ln -s"
            " /Applications/calibre.app/Contents/MacOS/ebook-convert"
            " /opt/homebrew/bin/ebook-convert"
        )

    dest = dest_dir / f"{src.stem}.epub"
    cover = generate_cover(src.stem, dest_dir / "cover.jpg")
    command = [
        "ebook-convert",
        str(src),
        str(dest),
        "--title",
        src.stem,
        "--cover",
        str(cover),
    ]
    if src.suffix.lower() in (".md", ".markdown", ".mkd", ".mdown"):
        # Calibre's default markdown extensions (footnotes,tables,toc) don't
        # include fenced_code, so ``` code blocks render as justified prose
        # instead of a monospace <pre> block.
        command.append("--markdown-extensions=footnotes,tables,toc,fenced_code")

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ebook-convert failed for {src} (exit {result.returncode}):\n{result.stderr}"
        )

    return dest
