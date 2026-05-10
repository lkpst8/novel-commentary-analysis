#!/usr/bin/env python3
"""Create and aggregate packet/phase note templates into reusable ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path

from workspace_utils import (
    dedupe_preserve_order,
    load_manifest,
    parse_bullets,
    parse_markdown_sections,
    render_bullets,
    write_text,
)


PACKET_NOTE_TEMPLATE = """# Packet {packet_number:03d} Notes

- Packet source: `{packet_path}`
- Fill this file once. Later steps should read this note file instead of reopening the packet unless you need to verify uncertainty.

## Story Role

- 

## Main Plot Events

- 

## Character Updates

- 

## Relationship Updates

- 

## World Or Background Updates

- 

## Subplot Updates

- 

## Foreshadowing Or Payoff

- 

## Ending Impact

- 

## Unresolved Threads

- 

## Source Certainty Notes

- 
"""


PHASE_NOTE_TEMPLATE = """# Phase {phase_number:02d} Notes

- Phase packets: {packet_start}-{packet_end}
- Fill this after completing the packet notes for this phase. Later compression should read this file before reading raw packets again.

## Main Plot Progress

- 

## Main Characters In Motion

- 

## Subplot Movement

- 

## Background Or World Updates

- 

## Turning Points

- 

## Ending Relevance

- 

## Unresolved Threads Carried Forward

- 

## Suggested One Paragraph Phase Summary

- 
"""


def ensure_note_templates(workspace_dir: Path, manifest: dict) -> None:
    packet_notes_dir = workspace_dir / "notes" / "packets"
    phase_notes_dir = workspace_dir / "notes" / "phases"
    packet_notes_dir.mkdir(parents=True, exist_ok=True)
    phase_notes_dir.mkdir(parents=True, exist_ok=True)

    for packet in manifest.get("packets", []):
        note_path = packet_notes_dir / f"packet-{int(packet['packet_number']):03d}-notes.md"
        if not note_path.exists():
            write_text(
                note_path,
                PACKET_NOTE_TEMPLATE.format(
                    packet_number=int(packet["packet_number"]),
                    packet_path=packet["relative_path"],
                ),
            )

    for phase in manifest.get("phases", []):
        note_path = phase_notes_dir / f"phase-{int(phase['phase_number']):02d}-notes.md"
        if not note_path.exists():
            write_text(
                note_path,
                PHASE_NOTE_TEMPLATE.format(
                    phase_number=int(phase["phase_number"]),
                    packet_start=int(phase["packet_start"]),
                    packet_end=int(phase["packet_end"]),
                ),
            )


def collect_section_bullets(markdown_path: Path, section_name: str) -> list[str]:
    if not markdown_path.exists():
        return []
    sections = parse_markdown_sections(markdown_path.read_text(encoding="utf-8"))
    return parse_bullets(sections.get(section_name, []))


def build_ledgers(workspace_dir: Path, manifest: dict) -> None:
    ledgers_dir = workspace_dir / "ledgers"
    ledgers_dir.mkdir(parents=True, exist_ok=True)

    packet_notes_dir = workspace_dir / "notes" / "packets"
    phase_notes_dir = workspace_dir / "notes" / "phases"

    character_updates: list[str] = []
    relationship_updates: list[str] = []
    subplot_updates: list[str] = []
    world_updates: list[str] = []
    foreshadow_updates: list[str] = []
    main_plot_updates: list[str] = []
    unresolved_threads: list[str] = []
    ending_impacts: list[str] = []

    for packet in manifest.get("packets", []):
        note_path = packet_notes_dir / f"packet-{int(packet['packet_number']):03d}-notes.md"
        packet_prefix = f"Packet {int(packet['packet_number']):03d}:"
        main_plot_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Main Plot Events")]
        )
        character_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Character Updates")]
        )
        relationship_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Relationship Updates")]
        )
        world_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "World Or Background Updates")]
        )
        subplot_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Subplot Updates")]
        )
        foreshadow_updates.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Foreshadowing Or Payoff")]
        )
        unresolved_threads.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Unresolved Threads")]
        )
        ending_impacts.extend(
            [f"{packet_prefix} {item}" for item in collect_section_bullets(note_path, "Ending Impact")]
        )

    phase_summaries_dir = workspace_dir / "phase-summaries"
    phase_summaries_dir.mkdir(parents=True, exist_ok=True)

    for phase in manifest.get("phases", []):
        note_path = phase_notes_dir / f"phase-{int(phase['phase_number']):02d}-notes.md"
        summary_path = phase_summaries_dir / f"phase-{int(phase['phase_number']):02d}-summary.md"
        sections = parse_markdown_sections(note_path.read_text(encoding="utf-8")) if note_path.exists() else {}
        summary_lines = [
            f"# Phase {int(phase['phase_number']):02d} Summary",
            "",
            f"- Packets: {int(phase['packet_start']):03d}-{int(phase['packet_end']):03d}",
            "",
            "## Main Plot Progress",
            "",
            render_bullets(parse_bullets(sections.get("Main Plot Progress", [])), "Not filled yet.").rstrip(),
            "",
            "## Main Characters In Motion",
            "",
            render_bullets(parse_bullets(sections.get("Main Characters In Motion", [])), "Not filled yet.").rstrip(),
            "",
            "## Subplot Movement",
            "",
            render_bullets(parse_bullets(sections.get("Subplot Movement", [])), "Not filled yet.").rstrip(),
            "",
            "## Background Or World Updates",
            "",
            render_bullets(parse_bullets(sections.get("Background Or World Updates", [])), "Not filled yet.").rstrip(),
            "",
            "## Turning Points",
            "",
            render_bullets(parse_bullets(sections.get("Turning Points", [])), "Not filled yet.").rstrip(),
            "",
            "## Ending Relevance",
            "",
            render_bullets(parse_bullets(sections.get("Ending Relevance", [])), "Not filled yet.").rstrip(),
            "",
            "## Unresolved Threads Carried Forward",
            "",
            render_bullets(parse_bullets(sections.get("Unresolved Threads Carried Forward", [])), "Not filled yet.").rstrip(),
            "",
        ]
        write_text(summary_path, "\n".join(summary_lines) + "\n")

    write_text(
        ledgers_dir / "main-plot-ledger.md",
        "# Main Plot Ledger\n\n"
        + render_bullets(dedupe_preserve_order(main_plot_updates), "No main-plot updates recorded yet."),
    )
    write_text(
        ledgers_dir / "character-ledger.md",
        "# Character Ledger\n\n"
        + render_bullets(dedupe_preserve_order(character_updates), "No character updates recorded yet."),
    )
    write_text(
        ledgers_dir / "relationship-ledger.md",
        "# Relationship Ledger\n\n"
        + render_bullets(dedupe_preserve_order(relationship_updates), "No relationship updates recorded yet."),
    )
    write_text(
        ledgers_dir / "subplot-ledger.md",
        "# Subplot Ledger\n\n"
        + render_bullets(dedupe_preserve_order(subplot_updates), "No subplot updates recorded yet."),
    )
    write_text(
        ledgers_dir / "world-ledger.md",
        "# World Ledger\n\n"
        + render_bullets(dedupe_preserve_order(world_updates), "No world or background updates recorded yet."),
    )
    write_text(
        ledgers_dir / "foreshadow-ledger.md",
        "# Foreshadow Ledger\n\n"
        + render_bullets(dedupe_preserve_order(foreshadow_updates), "No foreshadowing or payoff notes recorded yet."),
    )
    write_text(
        ledgers_dir / "ending-ledger.md",
        "# Ending Ledger\n\n"
        + render_bullets(dedupe_preserve_order(ending_impacts), "No ending-impact notes recorded yet."),
    )
    write_text(
        ledgers_dir / "unresolved-ledger.md",
        "# Unresolved Thread Ledger\n\n"
        + render_bullets(dedupe_preserve_order(unresolved_threads), "No unresolved threads recorded yet."),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reusable ledgers for a novel workspace.")
    parser.add_argument("workspace_dir", help="Path to a packetized novel workspace")
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    manifest = load_manifest(workspace_dir)
    ensure_note_templates(workspace_dir, manifest)
    build_ledgers(workspace_dir, manifest)
    print(f"Ledger workspace prepared in {workspace_dir}")


if __name__ == "__main__":
    main()
