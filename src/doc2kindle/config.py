import os
import tomllib
from pathlib import Path

REQUIRED_KEYS = ("smtp_host", "smtp_port", "smtp_from", "smtp_app_password", "kindle_to")


def _config_path() -> Path:
    override = os.environ.get("DOC2KINDLE_CONFIG")
    if override:
        return Path(override)
    xdg = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
    return Path(xdg) / "doc2kindle" / "config.toml"


def load() -> dict:
    path = _config_path()
    if not path.exists():
        raise RuntimeError(
            f"No config found at {path} — copy config.example.toml there "
            "(or point DOC2KINDLE_CONFIG at a different file) and fill in your values."
        )

    with open(path, "rb") as f:
        data = tomllib.load(f)

    missing = [key for key in REQUIRED_KEYS if not data.get(key)]
    if missing:
        raise RuntimeError(f"{path} is missing values: {', '.join(missing)}")

    return data
