#!/usr/bin/env python3
"""Detect chapter boundaries for raw novel sources or workspaces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from workspace_utils import (
    find_workspace_source,
    load_manifest,
    normalize_text,
    read_text,
    save_manifest,
    split_paragraphs,
    strip_html,
    write_text,
)


CHAPTER_PATTERNS = (
    re.compile(r"^第[0-9零一二三四五六七八九十百千万两]+[章节回卷部集篇幕].*$"),
    re.compile(r"^(chapter|prologue|epilogue)\b", re.IGNORECASE),
    re.compile(r"^(卷|番外|后记|序章|终章|楔子).*$"),
)


def detect_chapters(paragraphs: list[str]) -> list[dict]:
    chapters: list[dict] = []
    for index, paragraph in enumerate(paragraphs, start=1):
        sample = paragraph.strip()
        if len(sample) > 80:
            continue
        if any(pattern.match(sample) for pattern in CHAPTER_PATTERNS):
            chapters.append(
                {
                    "chapter_number": len(chapters) + 1,
                    "title": sample,
                    "start_paragraph": index,
                }
            )
    if not chapters:
        chapters.append(
            {
                "chapter_number": 1,
                "title": "Full Text",
                "start_paragraph": 1,
            }
        )

    for index, chapter in enumerate(chapters):
        next_start = (
            chapters[index + 1]["start_paragraph"] if index + 1 < len(chapters) else len(paragraphs) + 1
        )
        chapter["end_paragraph"] = next_start - 1
    return chapters


def chapter_to_packets(chapter: dict, packets: list[dict]) -> list[int]:
    packet_numbers: list[int] = []
    for packet in packets:
        if packet["end_paragraph"] < chapter["start_paragraph"]:
            continue
        if packet["start_paragraph"] > chapter["end_paragraph"]:
            continue
        packet_numbers.append(int(packet["packet_number"]))
    return packet_numbers


def render_markdown(chapters: list[dict], source_name: str) -> str:
    lines = [
        "# Chapter Index",
        "",
        f"- Source: `{source_name}`",
        f"- Detected chapters: {len(chapters)}",
        "",
        "| Chapter | Title | Paragraph Range | Packets |",
        "| --- | --- | --- | --- |",
    ]
    for chapter in chapters:
        packets = ", ".join(f"{number:03d}" for number in chapter.get("packets", [])) or "-"
        lines.append(
            f"| {chapter['chapter_number']} | {chapter['title']} | {chapter['start_paragraph']}-{chapter['end_paragraph']} | {packets} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect chapter boundaries for a novel workspace.")
    parser.add_argument("target", help="Workspace directory or raw source file")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    workspace_dir: Path | None = None
    manifest: dict | None = None

    if target.is_dir() and (target / "manifest.json").exists():
        workspace_dir = target
        manifest = load_manifest(workspace_dir)
        source_path = find_workspace_source(manifest)
        raw = read_text(source_path)
        packets = manifest.get("packets", [])
    else:
        source_path = target
        raw = read_text(source_path)
        packets = []

    if source_path.suffix.lower() in {".html", ".htm"}:
        raw = strip_html(raw)
    paragraphs = split_paragraphs(normalize_text(raw))
    chapters = detect_chapters(paragraphs)
    for chapter in chapters:
        chapter["packets"] = chapter_to_packets(chapter, packets)

    markdown = render_markdown(chapters, source_path.name)

    if workspace_dir is not None and manifest is not None:
        write_text(workspace_dir / "chapters.md", markdown)
        write_text(
            workspace_dir / "chapters.json",
            json.dumps(chapters, ensure_ascii=False, indent=2) + "\n",
        )
        manifest["chapters"] = chapters
        save_manifest(workspace_dir, manifest)
        print(f"Detected {len(chapters)} chapters in {workspace_dir}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
