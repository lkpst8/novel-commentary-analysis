#!/usr/bin/env python3
"""Split long novel text into a hierarchical analysis workspace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from workspace_utils import (
    normalize_text,
    read_text,
    sha1_text,
    split_paragraphs,
    strip_html,
    write_text,
)


CHAPTER_PATTERNS = (
    re.compile(r"^第[0-9零一二三四五六七八九十百千万两]+[章节回卷部集篇幕].*$"),
    re.compile(r"^(chapter|prologue|epilogue)\b", re.IGNORECASE),
)
SUPPORTED_SUFFIXES = {".txt", ".md", ".html", ".htm"}


def collect_sources(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.is_dir():
        raise RuntimeError(f"Input path does not exist: {target}")
    files = sorted(
        [path for path in target.rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES],
        key=lambda path: str(path).lower(),
    )
    if not files:
        raise RuntimeError(f"No supported source files found in {target}")
    return files


def load_source_bundle(target: Path) -> tuple[str, list[dict[str, str]]]:
    sources = collect_sources(target)
    parts: list[str] = []
    source_records: list[dict[str, str]] = []
    for path in sources:
        raw = read_text(path)
        if path.suffix.lower() in {".html", ".htm"}:
            raw = strip_html(raw)
        normalized = normalize_text(raw)
        parts.append(f"[[SOURCE:{path.name}]]\n\n{normalized}")
        source_records.append(
            {
                "name": path.name,
                "path": str(path.resolve()),
                "suffix": path.suffix.lower(),
            }
        )
    return "\n\n".join(part for part in parts if part.strip()), source_records


def is_chapter_heading(paragraph: str) -> bool:
    sample = paragraph.strip()
    if len(sample) > 60:
        return False
    return any(pattern.match(sample) for pattern in CHAPTER_PATTERNS)


def split_oversized_paragraph(paragraph: str, max_chars: int) -> list[str]:
    if len(paragraph) <= max_chars:
        return [paragraph]

    sentences = [
        chunk.strip()
        for chunk in re.split(r"(?<=[。！？!?；;])\s*", paragraph)
        if chunk.strip()
    ]
    if len(sentences) <= 1:
        return [paragraph[i : i + max_chars] for i in range(0, len(paragraph), max_chars)]

    pieces: list[str] = []
    current = ""
    for sentence in sentences:
        if current and len(current) + 1 + len(sentence) > max_chars:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    return pieces


def expand_paragraphs(paragraphs: list[str], max_chars: int) -> list[str]:
    expanded: list[str] = []
    for paragraph in paragraphs:
        expanded.extend(split_oversized_paragraph(paragraph, max_chars))
    return expanded


def packetize(paragraphs: list[str], max_chars: int) -> list[list[str]]:
    packets: list[list[str]] = []
    current: list[str] = []
    current_size = 0

    for paragraph in paragraphs:
        paragraph_size = len(paragraph)

        if current and is_chapter_heading(paragraph) and current_size >= max_chars // 2:
            packets.append(current)
            current = []
            current_size = 0

        if current and current_size + 2 + paragraph_size > max_chars:
            packets.append(current)
            current = []
            current_size = 0

        current.append(paragraph)
        current_size += paragraph_size + (2 if current_size else 0)

    if current:
        packets.append(current)

    return packets


def write_packet(
    packets_dir: Path,
    packet_number: int,
    title: str,
    source_name: str,
    packet: list[str],
    start_paragraph: int,
    total_paragraphs: int,
) -> dict[str, int | str]:
    body = "\n\n".join(packet)
    packet_name = f"packet-{packet_number:03d}.md"
    end_paragraph = start_paragraph + len(packet) - 1
    write_text(
        packets_dir / packet_name,
        "\n".join(
            [
                f"# {title} Packet {packet_number:03d}",
                "",
                f"- Source: `{source_name}`",
                f"- Paragraphs: {start_paragraph}-{end_paragraph} / {total_paragraphs}",
                f"- Characters: {len(body)}",
                "",
                "## Extraction Tasks",
                "",
                "- Record key events in chronological order.",
                "- Note any new named character or new role for an existing character.",
                "- Mark changes to background, institutions, factions, or world rules.",
                "- Flag subplot openings, escalations, merges, and closures.",
                "- Record unresolved threads that must be tracked later.",
                "",
                "## Text",
                "",
                body,
                "",
            ]
        )
        + "\n",
    )
    return {
        "packet_number": packet_number,
        "name": packet_name,
        "relative_path": f"packets/{packet_name}",
        "start_paragraph": start_paragraph,
        "end_paragraph": end_paragraph,
        "characters": len(body),
    }


def group_packets(
    packet_info: list[dict[str, int | str]], packets_per_phase: int
) -> list[dict[str, int | str]]:
    phases: list[dict[str, int | str]] = []
    for index in range(0, len(packet_info), packets_per_phase):
        group = packet_info[index : index + packets_per_phase]
        phase_number = len(phases) + 1
        phases.append(
            {
                "phase_number": phase_number,
                "packet_start": group[0]["packet_number"],
                "packet_end": group[-1]["packet_number"],
                "paragraph_start": group[0]["start_paragraph"],
                "paragraph_end": group[-1]["end_paragraph"],
                "characters": sum(int(item["characters"]) for item in group),
                "packets": [str(item["relative_path"]) for item in group],
            }
        )
    return phases


def write_phase_files(phases_dir: Path, phases: list[dict[str, int | str]], title: str) -> None:
    for phase in phases:
        phase_name = f"phase-{int(phase['phase_number']):02d}.md"
        packet_lines = [f"- `{packet}`" for packet in phase["packets"]]
        write_text(
            phases_dir / phase_name,
            "\n".join(
                [
                    f"# {title} Phase {int(phase['phase_number']):02d}",
                    "",
                    f"- Packets: {phase['packet_start']}-{phase['packet_end']}",
                    f"- Paragraphs: {phase['paragraph_start']}-{phase['paragraph_end']}",
                    f"- Approximate characters: {phase['characters']}",
                    "",
                    "## Included Packets",
                    "",
                    *packet_lines,
                    "",
                    "## Phase Summary Tasks",
                    "",
                    "- Summarize the main-line progress in this phase.",
                    "- List subplot changes introduced or resolved here.",
                    "- Record character-state changes for major figures.",
                    "- Note any new worldbuilding, institutions, factions, or rules.",
                    "- List unresolved threads that move into the next phase.",
                    "",
                ]
            )
            + "\n",
        )


def write_coverage_ledger(output_dir: Path, packet_info: list[dict[str, int | str]]) -> None:
    lines = [
        "# Coverage Ledger",
        "",
        "Use this file while reading very long novels. Every packet should be accounted for before you finalize the HTML output.",
        "",
        "| Packet | Story Stage | Main Plot Events | Subplot Updates | Character Changes | World/Background Notes | Unresolved Threads | Covered In Final HTML |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for info in packet_info:
        lines.append(f"| {int(info['packet_number']):03d} |  |  |  |  |  |  |  |")
    lines.append("")
    write_text(output_dir / "coverage-ledger.md", "\n".join(lines))


def write_html_outline_template(output_dir: Path, phases: list[dict[str, int | str]]) -> None:
    phase_lines = [
        f"- Phase {int(phase['phase_number']):02d}: packets {phase['packet_start']}-{phase['packet_end']}"
        for phase in phases
    ]
    write_text(
        output_dir / "html-outline-template.md",
        "\n".join(
            [
                "# HTML Outline Template",
                "",
                "Use this template to avoid losing important material when the novel is very long.",
                "",
                "## Page Architecture",
                "",
                "1. Header / hero summary",
                "2. One-screen quick answer: 这本书讲了什么",
                "3. Background and world rules",
                "4. Main-character roster",
                "5. Extended character/faction appendix when needed",
                "6. Relationship map summary",
                "7. Main plot overview in 6-12 stages",
                "8. Detailed act/phase breakdown",
                "9. Major subplots index",
                "10. Key turning points",
                "11. Ending and aftermath",
                "12. Themes and emotional core",
                "13. Memorable aspects",
                "14. Source certainty notes",
                "",
                "## Phase Coverage Checklist",
                "",
                *phase_lines,
                "",
                "## Anti-Omission Rules",
                "",
                "- Every phase must appear in either the main plot section or a clearly named subplot section.",
                "- Every major character should be introduced where they first become story-relevant.",
                "- Every subplot should have an opening, development, and closure state when the source allows it.",
                "- If the HTML becomes too long, compress wording before dropping events.",
                "- Use collapsible sections or appendices for secondary detail instead of deleting it.",
                "",
            ]
        ),
    )


def write_index(
    output_dir: Path,
    title: str,
    source_name: str,
    total_paragraphs: int,
    total_chars: int,
    packet_info: list[dict[str, int | str]],
    phases: list[dict[str, int | str]],
) -> None:
    lines = [
        f"# {title} Analysis Workspace",
        "",
        f"- Source: `{source_name}`",
        f"- Total paragraphs: {total_paragraphs}",
        f"- Total normalized characters: {total_chars}",
        f"- Total packets: {len(packet_info)}",
        f"- Total phases: {len(phases)}",
        "",
        "## Recommended Workflow For Very Long Novels",
        "",
        "1. Read packets in order and extract notes per packet.",
        "2. Merge packet notes into phase summaries.",
        "3. Maintain the coverage ledger so no packet is silently dropped.",
        "4. Build global character, relationship, world, and subplot notes.",
        "5. Draft the HTML from the outline template.",
        "6. Run a final pass to confirm every phase is represented.",
        "",
        "## Workspace Files",
        "",
        "- `packets/`: packet-by-packet source slices",
        "- `phases/`: grouped packet ranges for mid-level summaries",
        "- `coverage-ledger.md`: anti-omission tracker",
        "- `html-outline-template.md`: long-form HTML structure guide",
        "- `manifest.json`: machine-readable workspace metadata",
        "",
        "## Packets",
        "",
    ]
    for info in packet_info:
        lines.append(
            f"- `packets/packet-{int(info['packet_number']):03d}.md`: paragraphs {info['start_paragraph']}-{info['end_paragraph']}, {info['characters']} chars"
        )
    lines.extend(["", "## Phases", ""])
    for phase in phases:
        lines.append(
            f"- `phases/phase-{int(phase['phase_number']):02d}.md`: packets {phase['packet_start']}-{phase['packet_end']}, paragraphs {phase['paragraph_start']}-{phase['paragraph_end']}"
        )
    lines.append("")
    write_text(output_dir / "index.md", "\n".join(lines))


def write_manifest(
    output_dir: Path,
    source_path: Path,
    source_files: list[dict[str, str]],
    source_hash: str,
    title: str,
    total_paragraphs: int,
    total_chars: int,
    packet_info: list[dict[str, int | str]],
    phases: list[dict[str, int | str]],
    max_chars: int,
    packets_per_phase: int,
) -> None:
    manifest = {
        "title": title,
        "source_name": source_path.name,
        "source_path": str(source_path),
        "source_kind": "directory" if source_path.is_dir() else "file",
        "source_files": source_files,
        "source_hash": source_hash,
        "total_paragraphs": total_paragraphs,
        "total_characters": total_chars,
        "packet_count": len(packet_info),
        "phase_count": len(phases),
        "max_chars_per_packet": max_chars,
        "packets_per_phase": packets_per_phase,
        "packets": packet_info,
        "phases": phases,
    }
    write_text(
        output_dir / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )


def existing_workspace_matches(output_dir: Path, source_hash: str) -> bool:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except Exception:
        return False
    return manifest.get("source_hash") == source_hash


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a long novel into a packet and phase analysis workspace."
    )
    parser.add_argument("input_path", help="Path to a txt/html/md source file or a directory of source files")
    parser.add_argument("output_dir", help="Directory for generated workspace files")
    parser.add_argument("--title", help="Display title for generated packets")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Approximate maximum characters per packet",
    )
    parser.add_argument(
        "--packets-per-phase",
        type=int,
        default=6,
        help="How many packets to group into one mid-level phase summary",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild the workspace even if the source hash matches the existing manifest",
    )
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    output_dir = Path(args.output_dir).resolve()
    packets_dir = output_dir / "packets"
    phases_dir = output_dir / "phases"

    merged_text, source_files = load_source_bundle(input_path)
    source_hash = sha1_text(merged_text)

    if not args.force and existing_workspace_matches(output_dir, source_hash):
        print(f"Workspace already matches source hash in {output_dir}; reuse existing artifacts.")
        return

    packets_dir.mkdir(parents=True, exist_ok=True)
    phases_dir.mkdir(parents=True, exist_ok=True)

    paragraphs = split_paragraphs(merged_text)
    if not paragraphs:
        raise RuntimeError("No readable paragraphs found in source input.")

    title = args.title or input_path.stem
    max_chars = max(2000, args.max_chars)
    packets_per_phase = max(1, args.packets_per_phase)
    expanded_paragraphs = expand_paragraphs(paragraphs, max_chars)
    packets = packetize(expanded_paragraphs, max_chars=max_chars)

    packet_info: list[dict[str, int | str]] = []
    start_paragraph = 1
    source_name = input_path.name
    for index, packet in enumerate(packets, start=1):
        info = write_packet(
            packets_dir=packets_dir,
            packet_number=index,
            title=title,
            source_name=source_name,
            packet=packet,
            start_paragraph=start_paragraph,
            total_paragraphs=len(expanded_paragraphs),
        )
        packet_info.append(info)
        start_paragraph += len(packet)

    phases = group_packets(packet_info, packets_per_phase=packets_per_phase)
    write_phase_files(phases_dir, phases, title)
    write_coverage_ledger(output_dir, packet_info)
    write_html_outline_template(output_dir, phases)
    write_index(
        output_dir=output_dir,
        title=title,
        source_name=source_name,
        total_paragraphs=len(expanded_paragraphs),
        total_chars=len(merged_text),
        packet_info=packet_info,
        phases=phases,
    )
    write_manifest(
        output_dir=output_dir,
        source_path=input_path,
        source_files=source_files,
        source_hash=source_hash,
        title=title,
        total_paragraphs=len(expanded_paragraphs),
        total_chars=len(merged_text),
        packet_info=packet_info,
        phases=phases,
        max_chars=max_chars,
        packets_per_phase=packets_per_phase,
    )
    print(
        f"Generated workspace with {len(packet_info)} packets and {len(phases)} phases in {output_dir}"
    )


if __name__ == "__main__":
    main()
