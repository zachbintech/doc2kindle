# doc2kindle

Converts documents (Markdown, PDF, and anything Calibre's `ebook-convert` accepts)
to EPUB, then emails the result to a Kindle "Send to Kindle" address over Gmail SMTP.

Originated from [`personal` repo issue #4](https://github.com/zachbintech/personal/issues/4).

## Key files

- `main.py` — CLI entrypoint (symlinked onto `$PATH` as `doc2kindle`). Loops over
  input files, converts each into a temp dir, emails it, reports pass/fail.
- `convert.py` — `convert_to_epub(src, dest_dir)`, a thin wrapper around
  `ebook-convert`. No input-format allowlist; Calibre's own error surfaces for
  unsupported formats.
- `mailer.py` — `send_to_kindle(epub_path)`, sends the EPUB as an attachment via
  Gmail SMTP using values from `config.py`.
- `config.py` — gitignored, holds real SMTP/Kindle values. See
  `config.example.py` for the template and where each value comes from.

## Running it

```bash
doc2kindle report.pdf notes.md
```

Requires Calibre installed (`sudo apt install calibre`) and `config.py` filled in
(SMTP app password + Kindle send-to address).
