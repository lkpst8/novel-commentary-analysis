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


PLACEHOLDER_MARKERS = (
    "- Not filled yet.",
    "- No main-plot updates recorded yet.",
    "- No character updates recorded yet.",
    "- No relationship updates recorded yet.",
    "- No subplot updates recorded yet.",
    "- No world or background updates recorded yet.",
    "- No ending-impact notes recorded yet.",
)


def assert_workspace_coverage(workspace_dir: Path, manifest: dict, mode: str) -> None:
    packet_notes_dir = workspace_dir / "notes" / "packets"
    phase_notes_dir = workspace_dir / "notes" / "phases"
    ledgers_dir = workspace_dir / "ledgers"

    errors: list[str] = []

    for packet in manifest.get("packets", []):
        packet_number = int(packet["packet_number"])
        note_path = packet_notes_dir / f"packet-{packet_number:03d}-notes.md"
        if not note_path.exists():
            errors.append(f"Missing packet note: {note_path.name}")
            continue
        note_text = read_if_exists(note_path)
        if "\n- \n" in note_text or note_text.rstrip().endswith("-"):
            errors.append(f"Unfilled packet note: {note_path.name}")

    for phase in manifest.get("phases", []):
        phase_number = int(phase["phase_number"])
        note_path = phase_notes_dir / f"phase-{phase_number:02d}-notes.md"
        if not note_path.exists():
            errors.append(f"Missing phase note: {note_path.name}")
            continue
        note_text = read_if_exists(note_path)
        if "\n- \n" in note_text or note_text.rstrip().endswith("-"):
            errors.append(f"Unfilled phase note: {note_path.name}")

    required_ledgers = [
        "main-plot-ledger.md",
        "character-ledger.md",
        "relationship-ledger.md",
        "subplot-ledger.md",
        "world-ledger.md",
        "ending-ledger.md",
    ]
    for ledger_name in required_ledgers:
        ledger_path = ledgers_dir / ledger_name
        if not ledger_path.exists():
            errors.append(f"Missing ledger: {ledger_name}")
            continue
        ledger_text = read_if_exists(ledger_path)
        if any(marker in ledger_text for marker in PLACEHOLDER_MARKERS):
            errors.append(f"Ledger still looks unfilled: {ledger_name}")

    if errors:
        joined = "\n".join(f"- {item}" for item in errors)
        raise RuntimeError(
            f"Cannot build `{mode}` compression output because workspace coverage is incomplete.\n"
            f"{joined}\n"
            "Finish packet notes, phase notes, and ledgers first. "
            "Do not replace missing coverage by sampling a few packets."
        )


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
            "- This pass must not be built from sparse packet sampling. It requires full workspace coverage.",
            "",
            "## Compression Rules",
            "",
            "- Keep the opening situation, trigger, escalation, reversals, decision points, ending, and aftertaste.",
            "- Keep subplots only when they affect the main line, a major character arc, or the ending.",
            "- Shorten wording before deleting events.",
            "- If a later-phase revelation changes the meaning of earlier phases, reflect that here.",
            "- Do not build this pass by reading only the beginning, middle, and ending packets.",
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
            "- This pass must inherit from full coverage, not sparse sampling.",
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
            "- Never derive this pass from only a few sampled packets.",
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
        assert_workspace_coverage(workspace_dir, manifest, "full")
        write_text(workspace_dir / "compression-pass-1-full.md", build_full_pass(workspace_dir, manifest))
    if args.mode in ("all", "medium"):
        assert_workspace_coverage(workspace_dir, manifest, "medium")
        write_text(workspace_dir / "compression-pass-2-medium.md", build_medium_pass(workspace_dir))
    if args.mode in ("all", "short"):
        assert_workspace_coverage(workspace_dir, manifest, "short")
        write_text(workspace_dir / "compression-pass-3-short.md", build_short_pass(workspace_dir))
    if args.mode in ("all", "canon"):
        assert_workspace_coverage(workspace_dir, manifest, "canon")
        write_text(workspace_dir / "short-outline-canon.md", build_canon(workspace_dir))

    print(f"Compression artifacts updated in {workspace_dir}")


if __name__ == "__main__":
    main()
