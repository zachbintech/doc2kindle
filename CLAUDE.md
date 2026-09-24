# doc2kindle

Converts documents (Markdown, PDF, and anything Calibre's `ebook-convert` accepts)
to EPUB, then emails the result to a Kindle "Send to Kindle" address over Gmail SMTP.

Distributed as an installable package (`pipx install git+...`) exposing both a
CLI and an MCP server, so it's usable from any project, not just this repo.

Originated from [`personal` repo issue #4](https://github.com/zachbintech/personal/issues/4).

## Key files

- `src/doc2kindle/cli.py` — CLI entrypoint (`doc2kindle` console script). Loops
  over input files, converts each into a temp dir, emails it, reports pass/fail.
- `src/doc2kindle/mcp_server.py` — MCP server entrypoint (`doc2kindle-mcp`
  console script). Exposes one tool, `send_to_kindle(file_path)`.
- `src/doc2kindle/convert.py` — `convert_to_epub(src, dest_dir)`, a thin wrapper
  around `ebook-convert`. No input-format allowlist; Calibre's own error surfaces
  for unsupported formats.
- `src/doc2kindle/mailer.py` — `send_to_kindle(epub_path)`, sends the EPUB as an
  attachment via Gmail SMTP using values from `config.load()`.
- `src/doc2kindle/config.py` — loads TOML config from `~/.config/doc2kindle/config.toml`
  (or `$DOC2KINDLE_CONFIG`). Lives outside the repo/package since it's per-installer,
  not per-checkout. See `config.example.toml` for the template.

## Running it

```bash
doc2kindle report.pdf notes.md
```

Requires Calibre installed (Linux: `sudo apt install calibre`; macOS:
`brew install --cask calibre` plus symlinking `ebook-convert` from the app
bundle onto PATH — see README) and
`~/.config/doc2kindle/config.toml` filled in (SMTP app password + Kindle
send-to address) — see `config.example.toml`.

## Distribution

Installed via `pipx install git+ssh://git@github.com/zachbintech/doc2kindle.git`
(see README). No package index involved — every push to `main` is immediately
installable by re-running the same command with `--force`.
