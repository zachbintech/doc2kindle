# doc2kindle

Converts documents to EPUB and emails them to a Kindle "Send to Kindle" address over Gmail SMTP. It accepts Markdown, PDF and anything else Calibre's `ebook-convert` reads. It ships as an installable Python package with both a CLI (`doc2kindle`) and an MCP server (`doc2kindle-mcp`), so it works from any project. It started from [`personal` issue #4](https://github.com/zachbintech/personal/issues/4).

## Read first

- [`README.md`](README.md) covers install (Calibre + pipx), config, CLI usage and MCP registration.

## Commands

```bash
pip install -e .                       # dev install (Python ≥3.11); needs Calibre: sudo apt install calibre
doc2kindle report.pdf notes.md         # convert + email each file, reports pass/fail per file
claude mcp add doc2kindle --scope user -- doc2kindle-mcp
```

There is no test suite. To verify a change, send a real file to your own Kindle.

## Layout

All the code is in `src/doc2kindle/`:

- `cli.py` is the `doc2kindle` entry point. It converts each input into a temp dir and emails it.
- `mcp_server.py` is the `doc2kindle-mcp` entry point. It exposes one tool, `send_to_kindle(file_path)`.
- `convert.py` has `convert_to_epub(src, dest_dir)`, a thin wrapper around `ebook-convert`. It has no format allowlist, so Calibre's own error surfaces for unsupported formats.
- `cover.py` has `generate_cover(title, dest)`, which draws a plain title cover with Pillow. It falls back through the fonts, so it never fails over a missing font.
- `mailer.py` has `send_to_kindle(epub_path)`, which sends the EPUB as an attachment over Gmail SMTP.
- `config.py` loads TOML from `~/.config/doc2kindle/config.toml` (or `$DOC2KINDLE_CONFIG`). The config is per installer and lives outside the repo; `config.example.toml` is the template.

## Rules

- Keep the CLI and the MCP tool on the same `convert` and `mailer` path. Don't fork the logic.
- Never commit a real config: it holds the Gmail app password.
- Distribution is `pipx install git+…`, with no package index. Every push to `main` is immediately installable (`pipx install --force …`), so keep `main` working.
