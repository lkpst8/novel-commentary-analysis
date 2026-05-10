#!/usr/bin/env python3
"""Shared helpers for the novel commentary analysis workspace scripts."""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from typing import Iterable


ENCODINGS = ("utf-8", "utf-8-sig", "gb18030", "gbk")


def read_text(path: Path) -> str:
    last_error = None
    for encoding in ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise RuntimeError(f"Unable to decode {path} with known encodings: {last_error}")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<script\b.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style\b.*?</style>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</p\s*>", "\n\n", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    return html.unescape(raw)


def normalize_text(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = raw.replace("\u3000", " ")
    lines = [line.strip() for line in raw.split("\n")]
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if not line:
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        current.append(re.sub(r"\s+", " ", line))
    if current:
        paragraphs.append(" ".join(current).strip())
    return "\n\n".join(p for p in paragraphs if p)


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def load_manifest(workspace_dir: Path) -> dict:
    manifest_path = workspace_dir / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"manifest.json not found in {workspace_dir}")
    return json.loads(read_text(manifest_path))


def save_manifest(workspace_dir: Path, manifest: dict) -> None:
    write_text(
        workspace_dir / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip().lower())
    slug = slug.strip("-")
    return slug or "item"


def parse_markdown_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def parse_bullets(lines: Iterable[str]) -> list[str]:
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            values.append(stripped[2:].strip())
    return values


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            output.append(item)
    return output


def render_bullets(items: Iterable[str], empty_message: str) -> str:
    values = [item for item in items if item]
    if not values:
        return f"- {empty_message}\n"
    return "".join(f"- {item}\n" for item in values)


def find_workspace_source(manifest: dict) -> Path:
    return Path(manifest["source_path"]).resolve()
