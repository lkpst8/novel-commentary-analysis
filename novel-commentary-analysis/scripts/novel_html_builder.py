#!/usr/bin/env python3
"""Build a standalone HTML page from workspace ledgers and compression files."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from workspace_utils import load_manifest, read_text, write_text


def to_html_blocks(markdown_text: str) -> str:
    blocks: list[str] = []
    current_items: list[str] = []

    def flush_items() -> None:
        nonlocal current_items
        if current_items:
            blocks.append("<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in current_items) + "</ul>")
            current_items = []

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_items()
            continue
        if stripped.startswith("#"):
            flush_items()
            level = min(stripped.count("#"), 4)
            content = stripped[level:].strip()
            blocks.append(f"<h{level + 1}>{html.escape(content)}</h{level + 1}>")
        elif stripped.startswith("- "):
            current_items.append(stripped[2:].strip())
        else:
            flush_items()
            blocks.append(f"<p>{html.escape(stripped)}</p>")
    flush_items()
    return "\n".join(blocks)


def read_optional(path: Path, fallback: str) -> str:
    if path.exists():
        return read_text(path)
    return fallback


def build_html(workspace_dir: Path, title: str) -> str:
    manifest = load_manifest(workspace_dir)
    ledgers_dir = workspace_dir / "ledgers"

    snapshot = read_optional(workspace_dir / "compression-pass-2-medium.md", "Medium outline not built yet.")
    phase_breakdown = read_optional(workspace_dir / "compression-pass-1-full.md", "Full plot backbone not built yet.")
    characters = read_optional(ledgers_dir / "character-ledger.md", "Character ledger not built yet.")
    relationships = read_optional(ledgers_dir / "relationship-ledger.md", "Relationship ledger not built yet.")
    world = read_optional(ledgers_dir / "world-ledger.md", "World ledger not built yet.")
    main_plot = read_optional(ledgers_dir / "main-plot-ledger.md", "Main plot ledger not built yet.")
    subplots = read_optional(ledgers_dir / "subplot-ledger.md", "Subplot ledger not built yet.")
    foreshadow = read_optional(ledgers_dir / "foreshadow-ledger.md", "Foreshadow ledger not built yet.")
    ending = read_optional(ledgers_dir / "ending-ledger.md", "Ending ledger not built yet.")
    unresolved = read_optional(ledgers_dir / "unresolved-ledger.md", "Unresolved ledger not built yet.")
    short_outline = read_optional(workspace_dir / "short-outline-canon.md", "Short outline canon not built yet.")

    toc = [
        ("snapshot", "Story Snapshot"),
        ("background-world", "Background And World"),
        ("characters", "Character Roster"),
        ("relationships", "Relationship Overview"),
        ("main-plot", "Main Plot Timeline"),
        ("phase-breakdown", "Phase Breakdown"),
        ("subplots", "Major Subplots"),
        ("foreshadow", "Foreshadowing And Payoff"),
        ("ending", "Ending And Aftermath"),
        ("short-outline", "Short Outline Canon"),
        ("source-notes", "Certainty And Source Notes"),
    ]
    toc_html = "".join(f'<li><a href="#{section_id}">{label}</a></li>' for section_id, label in toc)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f5f0e7;
      --paper: #fffaf3;
      --ink: #1d252b;
      --muted: #5c676d;
      --line: #d3c7b8;
      --accent: #8f4b2e;
      --accent-soft: #e8d4c1;
      --shadow: 0 18px 40px rgba(42, 29, 17, 0.08);
      --max: 1180px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      font: 16px/1.75 "Microsoft YaHei", "PingFang SC", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(143, 75, 46, 0.10), transparent 26%),
        radial-gradient(circle at left 20%, rgba(83, 108, 116, 0.12), transparent 24%),
        linear-gradient(180deg, #f8f3ea 0%, var(--bg) 100%);
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    header {{
      padding: 64px 20px 40px;
      color: #f9f5ef;
      background: linear-gradient(135deg, #30474e, #182326);
    }}
    .wrap {{
      width: min(var(--max), calc(100% - 32px));
      margin: 0 auto;
    }}
    .eyebrow {{
      display: inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.08);
      font-size: 13px;
      letter-spacing: 0.06em;
    }}
    h1 {{ margin: 16px 0 12px; font-size: clamp(34px, 6vw, 64px); line-height: 1.08; }}
    .lead {{ max-width: 880px; color: rgba(249,245,239,0.9); }}
    .layout {{
      width: min(var(--max), calc(100% - 32px));
      margin: 0 auto;
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      gap: 24px;
      padding: 28px 0 56px;
    }}
    nav {{
      position: sticky;
      top: 18px;
      align-self: start;
      padding: 18px 18px 8px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: rgba(255,250,243,0.92);
      box-shadow: var(--shadow);
    }}
    nav ul {{ padding-left: 18px; margin: 0; }}
    nav li {{ margin: 0 0 10px; }}
    main {{
      display: grid;
      gap: 20px;
    }}
    section {{
      padding: 24px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--paper);
      box-shadow: var(--shadow);
    }}
    h2 {{ margin-top: 0; font-size: 28px; }}
    h3 {{ margin-top: 24px; font-size: 20px; }}
    p, li {{ color: var(--ink); }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}
    .meta span {{
      padding: 7px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.10);
      border: 1px solid rgba(255,255,255,0.14);
      font-size: 14px;
    }}
    .two-col {{
      display: grid;
      gap: 18px;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    details {{
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 14px 16px;
      background: #fffdf8;
    }}
    summary {{
      cursor: pointer;
      font-weight: 700;
      color: var(--accent);
    }}
    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      nav {{ position: static; }}
      .two-col {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <span class="eyebrow">Novel Commentary Analysis</span>
      <h1>{html.escape(title)}</h1>
      <p class="lead">Token-efficient long-novel analysis workspace rendered into a standalone HTML page. This page is built from ledgers and compression passes so later revisions do not need to re-read the full source every time.</p>
      <div class="meta">
        <span>Source: {html.escape(manifest["source_name"])}</span>
        <span>Packets: {manifest["packet_count"]}</span>
        <span>Phases: {manifest["phase_count"]}</span>
      </div>
    </div>
  </header>
  <div class="layout">
    <nav id="toc" aria-label="Table of contents">
      <h2>目录</h2>
      <ul>{toc_html}</ul>
    </nav>
    <main>
      <section id="snapshot">
        <h2>Story Snapshot</h2>
        {to_html_blocks(snapshot)}
      </section>
      <section id="background-world">
        <h2>Background And World</h2>
        {to_html_blocks(world)}
      </section>
      <section id="characters">
        <h2>Character Roster</h2>
        {to_html_blocks(characters)}
      </section>
      <section id="relationships">
        <h2>Relationship Overview</h2>
        {to_html_blocks(relationships)}
      </section>
      <section id="main-plot">
        <h2>Main Plot Timeline</h2>
        {to_html_blocks(main_plot)}
      </section>
      <section id="phase-breakdown">
        <h2>Phase Breakdown</h2>
        <details open>
          <summary>Expand full phase-by-phase breakdown</summary>
          {to_html_blocks(phase_breakdown)}
        </details>
      </section>
      <section id="subplots">
        <h2>Major Subplots</h2>
        {to_html_blocks(subplots)}
      </section>
      <section id="foreshadow">
        <h2>Foreshadowing And Payoff</h2>
        {to_html_blocks(foreshadow)}
      </section>
      <section id="ending">
        <h2>Ending And Aftermath</h2>
        {to_html_blocks(ending)}
      </section>
      <section id="short-outline">
        <h2>Short Outline Canon</h2>
        <details>
          <summary>Expand the fixed short-outline canon</summary>
          {to_html_blocks(short_outline)}
        </details>
      </section>
      <section id="source-notes">
        <h2>Certainty And Source Notes</h2>
        {to_html_blocks(unresolved)}
      </section>
    </main>
  </div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build standalone HTML from a novel workspace.")
    parser.add_argument("workspace_dir", help="Path to a packetized novel workspace")
    parser.add_argument(
        "--title",
        help="Optional HTML page title override",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path; defaults to final-html.html in the workspace",
    )
    args = parser.parse_args()

    workspace_dir = Path(args.workspace_dir).resolve()
    manifest = load_manifest(workspace_dir)
    title = args.title or manifest["title"]
    output_path = Path(args.output).resolve() if args.output else workspace_dir / "final-html.html"
    write_text(output_path, build_html(workspace_dir, title))
    print(f"HTML output written to {output_path}")


if __name__ == "__main__":
    main()
