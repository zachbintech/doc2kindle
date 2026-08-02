import shutil
import subprocess
from pathlib import Path


def convert_to_epub(src: Path, dest_dir: Path) -> Path:
    if shutil.which("ebook-convert") is None:
        raise RuntimeError(
            "ebook-convert not found on $PATH — install Calibre: sudo apt install calibre"
        )

    dest = dest_dir / f"{src.stem}.epub"
    result = subprocess.run(
        ["ebook-convert", str(src), str(dest), "--title", src.stem],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ebook-convert failed for {src} (exit {result.returncode}):\n{result.stderr}"
        )

    return dest
