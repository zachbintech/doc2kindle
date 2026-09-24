# doc2kindle

Converts Markdown, PDF, and other common document formats to EPUB and emails the result to a Kindle "Send to Kindle" address.

Started from [`personal` repo issue #4](https://github.com/zachbintech/personal/issues/4). Amazon's own Send-to-Kindle email service already accepts pdf/doc/docx/txt/rtf/html/epub directly, but it doesn't support Markdown at all, and its per-format handling (especially PDF reflow) is inconsistent. This tool converts everything to EPUB locally first (via Calibre's `ebook-convert`) for one consistent, controlled path, then emails the result.

Ships as both a CLI and an MCP server, so it can be installed once and used from any project.

## Status

Built and working — end-to-end tested against a real Kindle. See closed issues
in the repo's Issues tab for build history.

## Install

1. Install Calibre (provides `ebook-convert`):
   - Linux: `sudo apt install calibre`
   - macOS: `brew install --cask calibre`, then symlink the CLI onto your PATH
     (the app bundle doesn't add it):
     ```bash
     ln -s /Applications/calibre.app/Contents/MacOS/ebook-convert /opt/homebrew/bin/ebook-convert
     ```
2. Install the package with [pipx](https://pipx.pypa.io/) (or `uv tool install`):
   ```bash
   pipx install git+ssh://git@github.com/zachbintech/doc2kindle.git
   # or, over HTTPS:
   pipx install git+https://github.com/zachbintech/doc2kindle.git
   ```
   This puts both the `doc2kindle` CLI and `doc2kindle-mcp` MCP server on your `$PATH`.
3. Copy `config.example.toml` to `~/.config/doc2kindle/config.toml` and fill in
   your Gmail address, a [Gmail App Password](https://myaccount.google.com/apppasswords),
   and your Kindle send-to address. (Or point the `DOC2KINDLE_CONFIG` env var
   at a config file somewhere else.)
4. Add the sending Gmail address to your Kindle's approved senders: Amazon → Manage Your Content and Devices → Preferences → Personal Document Settings.

To pick up updates later, re-run the same `pipx install --force ...` command.

## Development install

To hack on a local clone, install it as an editable tool so edits take effect
immediately, without reinstalling:

```bash
git clone https://github.com/zachbintech/doc2kindle.git
uv tool install --editable ./doc2kindle   # or: pipx install -e ./doc2kindle
```

## CLI usage

```bash
doc2kindle ~/path/to/file.md
doc2kindle report.pdf notes.docx   # multiple files in one call
```

## MCP server

Register it once, at user scope, so it's available from every project:

```bash
claude mcp add doc2kindle --scope user -- doc2kindle-mcp
```

If Claude Code is ever launched from an environment where `~/.local/bin` isn't
on PATH (common for GUI-launched apps), register with the absolute path
instead: `claude mcp add doc2kindle --scope user -- ~/.local/bin/doc2kindle-mcp`

This exposes a single `send_to_kindle(file_path)` tool that converts a file
and emails it, using the same `~/.config/doc2kindle/config.toml` as the CLI.
