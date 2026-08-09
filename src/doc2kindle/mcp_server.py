import tempfile
from pathlib import Path

from mcp.server import MCPServer

from .convert import convert_to_epub
from .mailer import send_to_kindle as _send_to_kindle

mcp = MCPServer("doc2kindle")


@mcp.tool()
def send_to_kindle(file_path: str) -> str:
    """Convert a document (Markdown, PDF, or anything Calibre's ebook-convert
    accepts) to EPUB and email it to the configured Kindle address."""
    src = Path(file_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"No such file: {src}")

    with tempfile.TemporaryDirectory() as tmp:
        epub_path = convert_to_epub(src, Path(tmp))
        _send_to_kindle(epub_path)

    return f"Sent {src.name} to Kindle."


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
