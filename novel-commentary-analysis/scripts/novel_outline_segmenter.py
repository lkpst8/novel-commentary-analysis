#!/usr/bin/env python3
"""Plan segmented Markdown outline outputs from a prepared outline canon."""

from __future__ import annotations

import argparse
from pathlib import Path

from workspace_utils import load_manifest, read_text, write_text


def load_source_text(workspace_dir: Path, mode: str) -> tuple[Path, str]:
    if mode == "medium":
        path = workspace_dir / "compression-pass-2-medium.md"
    elif mode == "short":
        path = workspace_dir / "short-outline-canon.md"
    else:
        raise RuntimeError(f"Unsupported mode: {mode}")
    if not path.exists():
        raise RuntimeError(f"Required source file not found: {path.name}")
    return path, read_text(path)


def chunk_lines(text: str, max_lines: int) -> list[list[str]]:
    lines = text.splitlines()
    if not lines:
        return [[]]

    chunks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if current and len(current) >= max_lines and line.startswith("#"):
            chunks.append(current)
            current = []
        elif current and len(current) >= max_lines:
            chunks.append(current)
            current = []
        current.append(line)
    if current:
        chunks.append(current)
    return chunks


def build_segment_plan(workspace_dir: Path, mode: str, max_lines: int) -> tuple[list[dict], Path]:
    source_path, text = load_source_text(workspace_dir, mode)
    chunks = chunk_lines(text, max_lines=max_lines)
    output_dir = workspace_dir / "outline-parts" / mode
    output_dir.mkdir(parents=True, exist_ok=True)

    plan: list[dict] = []
    for index, lines in enumerate(chunks, start=1):
        part_name = f"{mode}-part-{index:02d}.md"
        part_path = output_dir / part_name
        plan.append(
            {
                "part_number": index,
                "file_name": part_name,
                "path": str(part_path),
                "line_count": len(lines),
            }
        )
    plan_path = output_dir / "segment-plan.md"
    write_text(
        plan_path,
        "\n".join(
            [
                f"# {mode} Segment Plan",
                "",
                f"- Source file: `{source_path.name}`",
                f"- Total parts: {len(plan)}",
                f"- Max lines per part: {max_lines}",
                "",
                "## Parts",
                "",
                *[
                    f"- Part {item['part_number']:02d}: `{item['file_name']}` ({item['line_count']} lines)"
                    for item in plan
                ],
                "",
                "## Usage Rule",
                "",
                "- Fill each part as a standalone Markdown file.",
                "- Keep the order fixed.",
                "- After all parts are ready, merge them with `scripts/novel_outline_merger.py`.",
                "",
            ]
        ),
    )
    return plan, plan_path


def write_part_templates(workspace_dir: Path, mode: str, plan: list[dict]) -> None:
    source_path, text = load_source_text(workspace_dir, mode)
    chunks = chunk_lines(text, max_lines=max(item["line_count"] for item in plan) if plan else 120)
    output_dir = workspace_dir / "outline-parts" / mode

    for item, chunk in zip(plan, chunks):
        part_path = output_dir / item["file_name"]
        write_text(
            part_path,
            "\n".join(
                [
                    f"# {mode} Part {item['part_number']:02d}",
                    "",
                    f"- Source: `{source_path.name}`",
                    "- Replace this template body with the final polished Markdown for this part.",
                    "- Keep the content faithful to the prepared source text below.",
                    "",
                    "## Source Slice",
                    "",
                    *chunk,
                    "",
                ]
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare segmented Markdown outline parts.")
    parser.add_argument("workspace_dir", help="Path to a novel workspace")
    parser.add_argument(
        "--mode",
        choices=("medium", "short"),
        required=True,
        help="Which outline mode to segment",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=120,
        help="Approximate maximum lines per part template",
    )
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    load_manifest(workspace_dir)
    plan, plan_path = build_segment_plan(workspace_dir, args.mode, args.max_lines)
    write_part_templates(workspace_dir, args.mode, plan)
    print(f"Segment plan written to {plan_path}")


if __name__ == "__main__":
    main()
