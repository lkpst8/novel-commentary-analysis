#!/usr/bin/env python3
"""Build reusable compression passes for medium and short novel outlines."""

from __future__ import annotations

import argparse
from pathlib import Path

from workspace_utils import load_manifest, read_text, write_text


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return read_text(path).strip()


def build_phase_index(workspace_dir: Path, manifest: dict) -> str:
    phase_summaries_dir = workspace_dir / "phase-summaries"
    lines: list[str] = []
    for phase in manifest.get("phases", []):
        phase_number = int(phase["phase_number"])
        phase_path = phase_summaries_dir / f"phase-{phase_number:02d}-summary.md"
        lines.append(f"## Phase {phase_number:02d}")
        lines.append("")
        lines.append(
            f"- Packet range: {int(phase['packet_start']):03d}-{int(phase['packet_end']):03d}"
        )
        lines.append("")
        lines.append(read_if_exists(phase_path) or "- Phase summary not available yet.")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_full_pass(workspace_dir: Path, manifest: dict) -> str:
    ledgers_dir = workspace_dir / "ledgers"
    return "\n".join(
        [
            "# Compression Pass 1 - Full Plot Backbone",
            "",
            "- Goal: retain the complete causal chain of the novel before any heavy compression.",
            "- Read this file before creating medium or short outlines.",
            "- Use phase summaries and ledgers first. Re-open raw packets only when a crucial ambiguity remains unresolved.",
            "",
            "## Story Scope",
            "",
            f"- Source: `{manifest['source_name']}`",
            f"- Packets: {manifest['packet_count']}",
            f"- Phases: {manifest['phase_count']}",
            "",
            "## Main Plot Backbone",
            "",
            read_if_exists(ledgers_dir / "main-plot-ledger.md") or "- Main plot ledger not built yet.",
            "",
            "## Phase Breakdown",
            "",
            build_phase_index(workspace_dir, manifest),
            "",
            "## Character Arc Ledger",
            "",
            read_if_exists(ledgers_dir / "character-ledger.md") or "- Character ledger not built yet.",
            "",
            "## Subplot Ledger",
            "",
            read_if_exists(ledgers_dir / "subplot-ledger.md") or "- Subplot ledger not built yet.",
            "",
            "## Ending And Resolution Ledger",
            "",
            read_if_exists(ledgers_dir / "ending-ledger.md") or "- Ending ledger not built yet.",
            "",
            "## Remaining Uncertainties",
            "",
            read_if_exists(ledgers_dir / "unresolved-ledger.md") or "- Unresolved ledger not built yet.",
            "",
        ]
    ).strip() + "\n"


def build_medium_pass(workspace_dir: Path) -> str:
    full_pass = read_if_exists(workspace_dir / "compression-pass-1-full.md")
    return "\n".join(
        [
            "# Compression Pass 2 - Medium Outline",
            "",
            "- Goal: compress the novel into a readable mid-length outline while preserving the full main-line causality.",
            "- Merge repetitive beats before dropping anything important.",
            "- Keep every ending-relevant character, subplot, and reversal.",
            "",
            "## Compression Rules",
            "",
            "- Keep the opening situation, trigger, escalation, reversals, decision points, ending, and aftertaste.",
            "- Keep subplots only when they affect the main line, a major character arc, or the ending.",
            "- Shorten wording before deleting events.",
            "- If a later-phase revelation changes the meaning of earlier phases, reflect that here.",
            "",
            "## Source Material",
            "",
            full_pass or "- Full pass not available yet.",
            "",
        ]
    ).strip() + "\n"


def build_short_pass(workspace_dir: Path) -> str:
    medium_pass = read_if_exists(workspace_dir / "compression-pass-2-medium.md")
    return "\n".join(
        [
            "# Compression Pass 3 - Short Outline",
            "",
            "- Goal: rebuild the long novel as a short-form complete story skeleton.",
            "- This is not a list of fragments. It should read like a compact but complete narrative arc.",
            "",
            "## Required Skeleton",
            "",
            "1. Opening situation",
            "2. Triggering event",
            "3. Main conflict escalation",
            "4. Midpoint reversal",
            "5. Late major turn",
            "6. Final decision or confrontation",
            "7. Ending and residue",
            "",
            "## Compression Rules",
            "",
            "- Do not invent bridge scenes between preserved events.",
            "- Do not keep minor atmosphere scenes unless they materially shape the story arc.",
            "- Do not let the back half collapse into two vague sentences.",
            "- Every preserved subplot must visibly affect the short outline.",
            "",
            "## Source Material",
            "",
            medium_pass or "- Medium pass not available yet.",
            "",
        ]
    ).strip() + "\n"


def build_canon(workspace_dir: Path) -> str:
    short_pass = read_if_exists(workspace_dir / "compression-pass-3-short.md")
    return "\n".join(
        [
            "# Short Outline Canon",
            "",
            "- Use this as the fixed source when the final short outline must be emitted across multiple model outputs.",
            "- Later segmented outputs should cite this canon rather than reopening the full workspace.",
            "",
            "## Canon Story Skeleton",
            "",
            short_pass or "- Short pass not available yet.",
            "",
            "## Segmented Output Plan",
            "",
            "- Part 1: opening situation through mid-story escalation",
            "- Part 2: midpoint through late major turn",
            "- Part 3: final decision, ending, and thematic residue",
            "",
        ]
    ).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create compression passes for a novel workspace.")
    parser.add_argument("workspace_dir", help="Path to a packetized novel workspace")
    parser.add_argument(
        "--mode",
        choices=("all", "full", "medium", "short", "canon"),
        default="all",
        help="Which compression artifact to build",
    )
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    manifest = load_manifest(workspace_dir)

    if args.mode in ("all", "full"):
        write_text(workspace_dir / "compression-pass-1-full.md", build_full_pass(workspace_dir, manifest))
    if args.mode in ("all", "medium"):
        write_text(workspace_dir / "compression-pass-2-medium.md", build_medium_pass(workspace_dir))
    if args.mode in ("all", "short"):
        write_text(workspace_dir / "compression-pass-3-short.md", build_short_pass(workspace_dir))
    if args.mode in ("all", "canon"):
        write_text(workspace_dir / "short-outline-canon.md", build_canon(workspace_dir))

    print(f"Compression artifacts updated in {workspace_dir}")


if __name__ == "__main__":
    main()
