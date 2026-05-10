#!/usr/bin/env python3
"""Merge segmented Markdown outline parts into one final Markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from workspace_utils import load_manifest, read_text, write_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge segmented outline Markdown parts.")
    parser.add_argument("workspace_dir", help="Path to a novel workspace")
    parser.add_argument(
        "--mode",
        choices=("medium", "short"),
        required=True,
        help="Which outline mode to merge",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path; defaults to medium-outline.md or short-outline.md in the workspace",
    )
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    load_manifest(workspace_dir)

    parts_dir = workspace_dir / "outline-parts" / args.mode
    if not parts_dir.exists():
        raise RuntimeError(f"Segmented parts directory not found: {parts_dir}")

    part_files = sorted(parts_dir.glob(f"{args.mode}-part-*.md"))
    if not part_files:
        raise RuntimeError(f"No part files found in {parts_dir}")

    merged_blocks: list[str] = []
    for path in part_files:
        merged_blocks.append(read_text(path).strip())

    output_name = "medium-outline.md" if args.mode == "medium" else "short-outline.md"
    output_path = Path(args.output).resolve() if args.output else workspace_dir / output_name
    write_text(output_path, "\n\n".join(block for block in merged_blocks if block) + "\n")
    print(f"Merged {len(part_files)} parts into {output_path}")


if __name__ == "__main__":
    main()
