# doc2kindle

Converts Markdown, PDF, and other common document formats to EPUB and emails the result to a Kindle "Send to Kindle" address.

Started from [`personal` repo issue #4](https://github.com/zachbintech/personal/issues/4). Amazon's own Send-to-Kindle email service already accepts pdf/doc/docx/txt/rtf/html/epub directly, but it doesn't support Markdown at all, and its per-format handling (especially PDF reflow) is inconsistent. This tool converts everything to EPUB locally first (via Calibre's `ebook-convert`) for one consistent, controlled path, then emails the result.

## Status

Built and working — end-to-end tested against a real Kindle. See closed issues
in the repo's Issues tab for build history.

## Usage

```bash
doc2kindle ~/path/to/file.md
doc2kindle report.pdf notes.docx   # multiple files in one call
```

## Setup

1. Install Calibre (provides `ebook-convert`): `sudo apt install calibre`
2. Copy `config.example.py` to `config.py` and fill in your Gmail address, a [Gmail App Password](https://myaccount.google.com/apppasswords), and your Kindle send-to address.
3. Add the sending Gmail address to your Kindle's approved senders: Amazon → Manage Your Content and Devices → Preferences → Personal Document Settings.
4. Symlink `main.py` onto your `$PATH` as `doc2kindle`.
