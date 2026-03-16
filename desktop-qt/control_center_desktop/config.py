from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


def _default_config_path() -> Path:
    return Path.home() / ".control_center" / "desktop_config.json"


@dataclass
class DesktopConfig:
    api_base_url: str = "http://127.0.0.1:8000"
    access_token: str | None = None

    @classmethod
    def load(cls, path: Path | None = None) -> "DesktopConfig":
        path = path or _default_config_path()
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return cls()
        return cls(
            api_base_url=data.get("api_base_url") or cls.api_base_url,
            access_token=data.get("access_token"),
        )

    def save(self, path: Path | None = None) -> None:
        path = path or _default_config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "api_base_url": self.api_base_url,
                    "access_token": self.access_token,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

