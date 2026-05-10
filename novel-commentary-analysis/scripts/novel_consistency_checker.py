#!/usr/bin/env python3
"""Run structural checks against a novel analysis workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from workspace_utils import load_manifest, read_text, write_text


REQUIRED_PACKET_NOTE_SECTIONS = [
    "Story Role",
    "Main Plot Events",
    "Character Updates",
    "Relationship Updates",
    "World Or Background Updates",
    "Subplot Updates",
    "Foreshadowing Or Payoff",
    "Ending Impact",
    "Unresolved Threads",
]


REQUIRED_HTML_IDS = [
    "snapshot",
    "background-world",
    "characters",
    "relationships",
    "main-plot",
    "phase-breakdown",
    "subplots",
    "ending",
    "short-outline",
    "source-notes",
]


def missing_sections(text: str, section_names: list[str]) -> list[str]:
    missing: list[str] = []
    for name in section_names:
        if f"## {name}" not in text:
            missing.append(name)
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a novel commentary workspace for omissions.")
    parser.add_argument("workspace_dir", help="Path to a packetized novel workspace")
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    manifest = load_manifest(workspace_dir)

    warnings: list[str] = []
    packet_notes_dir = workspace_dir / "notes" / "packets"
    phase_notes_dir = workspace_dir / "notes" / "phases"
    phase_summaries_dir = workspace_dir / "phase-summaries"
    ledgers_dir = workspace_dir / "ledgers"

    for packet in manifest.get("packets", []):
        packet_number = int(packet["packet_number"])
        note_path = packet_notes_dir / f"packet-{packet_number:03d}-notes.md"
        if not note_path.exists():
            warnings.append(f"Missing packet note file: {note_path.name}")
            continue
        note_text = read_text(note_path)
        missing = missing_sections(note_text, REQUIRED_PACKET_NOTE_SECTIONS)
        if missing:
            warnings.append(f"{note_path.name} missing sections: {', '.join(missing)}")
        if "\n- \n" in note_text or note_text.rstrip().endswith("-"):
            warnings.append(f"{note_path.name} still contains unfilled bullet placeholders.")

    for phase in manifest.get("phases", []):
        phase_number = int(phase["phase_number"])
        note_path = phase_notes_dir / f"phase-{phase_number:02d}-notes.md"
        summary_path = phase_summaries_dir / f"phase-{phase_number:02d}-summary.md"
        if not note_path.exists():
            warnings.append(f"Missing phase note file: {note_path.name}")
        if not summary_path.exists():
            warnings.append(f"Missing phase summary file: {summary_path.name}")

    for ledger_name in (
        "main-plot-ledger.md",
        "character-ledger.md",
        "relationship-ledger.md",
        "subplot-ledger.md",
        "world-ledger.md",
        "ending-ledger.md",
    ):
        if not (ledgers_dir / ledger_name).exists():
            warnings.append(f"Missing ledger file: {ledger_name}")

    full_pass = workspace_dir / "compression-pass-1-full.md"
    medium_pass = workspace_dir / "compression-pass-2-medium.md"
    short_pass = workspace_dir / "compression-pass-3-short.md"
    canon = workspace_dir / "short-outline-canon.md"
    for path in (full_pass, medium_pass, short_pass, canon):
        if not path.exists():
            warnings.append(f"Missing compression artifact: {path.name}")

    html_path = workspace_dir / "final-html.html"
    if html_path.exists():
        html_text = read_text(html_path)
        for section_id in REQUIRED_HTML_IDS:
            if f'id="{section_id}"' not in html_text:
                warnings.append(f"final-html.html is missing section id `{section_id}`.")
    else:
        warnings.append("final-html.html has not been built yet.")

    coverage_path = workspace_dir / "coverage-ledger.md"
    if coverage_path.exists():
        coverage_text = read_text(coverage_path)
        if "| Covered In Final HTML |" not in coverage_text:
            warnings.append("coverage-ledger.md does not contain the final coverage column.")
    else:
        warnings.append("coverage-ledger.md is missing.")

    report_lines = [
        "# Consistency Check Report",
        "",
        f"- Workspace: `{workspace_dir}`",
        f"- Packets: {manifest['packet_count']}",
        f"- Phases: {manifest['phase_count']}",
        "",
    ]
    if warnings:
        report_lines.append("## Warnings")
        report_lines.append("")
        report_lines.extend(f"- {warning}" for warning in warnings)
    else:
        report_lines.append("## Result")
        report_lines.append("")
        report_lines.append("- No structural issues detected.")
    report_lines.append("")

    report_path = workspace_dir / "consistency-report.md"
    write_text(report_path, "\n".join(report_lines))
    print(f"Consistency report written to {report_path}")


if __name__ == "__main__":
    main()
