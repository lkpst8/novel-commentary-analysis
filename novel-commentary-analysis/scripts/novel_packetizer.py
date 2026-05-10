#!/usr/bin/env python3
"""Split long novel text into analysis-friendly markdown packets."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ENCODINGS = ("utf-8", "utf-8-sig", "gb18030", "gbk")


def read_text(path: Path) -> str:
    last_error = None
    for encoding in ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise RuntimeError(f"Unable to decode {path} with known encodings: {last_error}")


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<script\\b.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style\\b.*?</style>", " ", raw)
    raw = re.sub(r"(?i)<br\\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</p\\s*>", "\n\n", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return raw


def normalize_text(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = raw.replace("\u3000", " ")
    lines = [line.strip() for line in raw.split("\n")]
    paragraphs = []
    current = []
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


def packetize(paragraphs: list[str], max_chars: int) -> list[list[str]]:
    packets: list[list[str]] = []
    current: list[str] = []
    current_size = 0

    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
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
    output_dir: Path,
    packet_number: int,
    title: str,
    source_name: str,
    packet: list[str],
    start_paragraph: int,
    total_paragraphs: int,
) -> dict[str, int | str]:
    body = "\n\n".join(packet)
    packet_name = f"packet-{packet_number:03d}.md"
    packet_path = output_dir / packet_name
    end_paragraph = start_paragraph + len(packet) - 1
    packet_path.write_text(
        "\n".join(
            [
                f"# {title} Packet {packet_number:03d}",
                "",
                f"- Source: `{source_name}`",
                f"- Paragraphs: {start_paragraph}-{end_paragraph} / {total_paragraphs}",
                f"- Characters: {len(body)}",
                "",
                "## Reading Focus",
                "",
                "- Record key events and immediate causes.",
                "- Note any new character, relationship shift, or tonal change.",
                "- Mark unresolved threads to revisit after later packets.",
                "",
                "## Text",
                "",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "name": packet_name,
        "start_paragraph": start_paragraph,
        "end_paragraph": end_paragraph,
        "characters": len(body),
    }


def write_index(
    output_dir: Path,
    title: str,
    source_name: str,
    total_paragraphs: int,
    packet_info: list[dict[str, int | str]],
) -> None:
    lines = [
        f"# {title} Packet Index",
        "",
        f"- Source: `{source_name}`",
        f"- Total paragraphs: {total_paragraphs}",
        f"- Total packets: {len(packet_info)}",
        "",
        "## Suggested Workflow",
        "",
        "1. Read one packet at a time.",
        "2. Extract events, motives, conflicts, and emotional shifts.",
        "3. Maintain a running timeline and character map.",
        "4. Synthesize across all packets only after the full pass.",
        "",
        "## Packets",
        "",
    ]

    for info in packet_info:
        lines.append(
            f"- `{info['name']}`: paragraphs {info['start_paragraph']}-{info['end_paragraph']}, {info['characters']} chars"
        )

    lines.append("")
    (output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a long novel into markdown packets.")
    parser.add_argument("input_path", help="Path to a txt/html/md source file")
    parser.add_argument("output_dir", help="Directory for generated packet files")
    parser.add_argument("--title", help="Display title for generated packets")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Approximate maximum characters per packet",
    )
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = read_text(input_path)
    if input_path.suffix.lower() in {".html", ".htm"}:
        raw = strip_html(raw)
    text = normalize_text(raw)
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        raise RuntimeError("No readable paragraphs found in source file.")

    title = args.title or input_path.stem
    packets = packetize(paragraphs, max_chars=max(2000, args.max_chars))

    packet_info = []
    start_paragraph = 1
    for index, packet in enumerate(packets, start=1):
        info = write_packet(
            output_dir=output_dir,
            packet_number=index,
            title=title,
            source_name=input_path.name,
            packet=packet,
            start_paragraph=start_paragraph,
            total_paragraphs=len(paragraphs),
        )
        packet_info.append(info)
        start_paragraph += len(packet)

    write_index(output_dir, title, input_path.name, len(paragraphs), packet_info)
    print(f"Generated {len(packet_info)} packets in {output_dir}")


if __name__ == "__main__":
    main()
