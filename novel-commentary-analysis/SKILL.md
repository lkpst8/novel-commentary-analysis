---
name: novel-commentary-analysis
description: Analyze long novels with a token-efficient staged workflow and generate either complete HTML commentary pages or compressed plot outlines. Use when Codex needs to process full-length fiction from `.txt`, `.md`, `.html`, chapter dumps, multi-file novel folders, or pasted excerpts and output a structured analysis covering 人物, 背景, 世界观, 主线剧情, 支线剧情, 关键转折, 结局, 主题, or a short-form complete plot outline. Use especially when the source is very long and the work must stay faithful to the text without inventing scenes, motives, bridge events, settings, or endings.
---

# Novel Commentary Analysis

## Overview

Use this skill to process novels in a staged, reusable way instead of repeatedly rereading the same source text. The skill supports two major deliverables:

- `full-html`: a complete HTML analysis page
- `short-outline`: a compressed short-form plot outline that preserves the whole story arc

It also supports:

- `medium-outline`: a mid-length bridge between the full analysis and the short outline

The core design goal is token efficiency. Read the raw source once into a workspace, then make later steps consume packet notes, phase summaries, ledgers, and compression artifacts rather than sending the entire novel back through the model.

## Modes

Choose one mode before drafting:

- `full-html`
  Use when the user wants a complete HTML page that clearly explains what the novel is about, who matters, how the world works, what the main line is, what the major subplots are, and how the ending lands.

- `medium-outline`
  Use when the user wants a readable but compressed full-book outline that preserves the whole causal chain without the size of the full HTML page.

- `short-outline`
  Use when the user wants the novel compressed into a short-form complete story skeleton. This should still preserve opening situation, trigger, escalation, turning points, ending, and residue.

If the user does not specify a mode, default to `full-html`.

## Non-Negotiable Fidelity Rules

Strictly obey these rules:

- Do not invent scenes, motives, settings, timelines, outcomes, or relationships not supported by the source.
- Do not create bridge events just to make compression smoother.
- Do not turn weak implication into certainty.
- Do not silently fix broken chronology in the source.
- Do not inflate a minor side plot into a major narrative line.
- If the source is incomplete or dirty, say exactly where certainty drops.

Use these labels when needed:

- `原文明确`
- `分析判断`
- `材料不足`

If a section cannot be filled from available material, keep the section and state `原文材料不足，暂不下结论`.

## Anti-Omission Rules

For large novels, omission is as dangerous as hallucination.

Before finalizing any major output, confirm:

- every packet is represented somewhere in the notes or ledgers
- every phase appears in the final understanding of the story
- every major character has an explicit role and final state when source permits
- every major subplot has start, development, and closure status when source permits
- the ending reflects late-book events, not just the premise or first half

If you cannot verify those points, do not finalize.

## Token Efficiency Rules

Use the workspace to avoid repeated raw-text input:

1. Read the raw source once to build a workspace.
2. Fill packet notes once.
3. Build ledgers from notes.
4. Build compression passes from ledgers and phase summaries.
5. Build final HTML or outlines from those artifacts.

After the workspace exists:

- Prefer `manifest.json`, `chapters.md`, packet notes, phase notes, ledgers, and compression passes.
- Reopen raw packets only when a real ambiguity remains unresolved.
- Do not resummarize the entire novel from scratch if the workspace artifacts already cover it.

This skill should treat the raw novel as the expensive input and the workspace as the reusable memory layer.

## Intake

Identify:

- source type: raw file, multi-file novel folder, excerpt, or existing workspace
- desired mode: `full-html`, `medium-outline`, or `short-outline`
- coverage: whole novel, selected arc, character line, relationship line, or theme
- spoiler policy: full spoilers, limited spoilers, or spoiler-free
- source certainty: complete, partial, or damaged

If the input is already a workspace with `manifest.json`, continue from the workspace instead of rebuilding it.

## Normal-Length Workflow

Use this when the source is short enough that omission risk is moderate:

1. Packetize if needed.
2. Create packet notes.
3. Build ledgers.
4. Build compression passes.
5. Generate the requested output.
6. Run consistency checks.

## Very-Long-Novel Workflow

Use this for multi-megabyte or tens-of-megabytes novels:

1. Run `scripts/novel_packetizer.py`.
2. Run `scripts/novel_chapter_detector.py`.
3. Fill packet notes under `notes/packets/`.
4. Fill phase notes under `notes/phases/`.
5. Run `scripts/novel_ledger_builder.py`.
6. Run `scripts/novel_outline_compressor.py`.
7. Run either `scripts/novel_html_builder.py` or use the short-outline canon.
8. Run `scripts/novel_consistency_checker.py`.

For very long novels, do not skip the note and ledger layers. They are the token-saving mechanism.

## `full-html` Rules

The final HTML should help a new reader quickly understand:

- the background
- the world or institutional logic
- the major characters
- the relationship structure
- the main plot
- the important subplots
- the turning points
- the ending and aftermath
- the themes and emotional core

Unless the user narrows the task, include:

1. title block
2. story snapshot
3. background and world
4. character roster
5. relationship overview
6. main plot timeline
7. phase-by-phase breakdown
8. major subplots
9. key turning points
10. ending and aftermath
11. themes and emotional core
12. certainty and source notes

For very long novels, also include:

- quick navigation
- appendix-friendly overflow handling
- optional cast/faction appendix
- optional detailed chronology appendix

Use [references/html-output-spec.md](references/html-output-spec.md).

## `medium-outline` Rules

This mode should preserve the entire main-line causality in a compressed form.

Keep:

- opening state
- trigger
- escalation
- major reversals
- ending
- major character landing points
- ending-relevant subplots

Compress:

- repeated bridge scenes
- repetitive atmosphere beats
- minor incidents that do not change story direction

Always build this from ledgers and the full compression pass first.

## `short-outline` Rules

This mode rebuilds the long novel as a short-form complete plot skeleton.

It must still contain:

1. opening situation
2. triggering event
3. central escalation
4. midpoint or major reversal
5. late major turn
6. final decision or confrontation
7. ending and residue

Build it through stages:

1. `compression-pass-1-full.md`
2. `compression-pass-2-medium.md`
3. `compression-pass-3-short.md`
4. `short-outline-canon.md`

If the final short outline exceeds one output window, emit it in parts from the canon instead of continuing from memory.

Use [references/short-outline-spec.md](references/short-outline-spec.md).

## Output Verification

Before returning results, verify:

- no invented events or motives were added
- main plot and subplots are not confused
- the ending matches the known source
- late-book events are not erased by compression
- each phase is represented in the final understanding
- the output was built from workspace artifacts where possible instead of repeated raw-text rereads

If these checks fail, fix the draft before returning it.

## Tools And References

Scripts:

- `scripts/novel_packetizer.py`
- `scripts/novel_chapter_detector.py`
- `scripts/novel_ledger_builder.py`
- `scripts/novel_outline_compressor.py`
- `scripts/novel_html_builder.py`
- `scripts/novel_consistency_checker.py`

References:

- [references/commentary-framework.md](references/commentary-framework.md)
- [references/html-output-spec.md](references/html-output-spec.md)
- [references/large-novel-scaling.md](references/large-novel-scaling.md)
- [references/ledger-spec.md](references/ledger-spec.md)
- [references/short-outline-spec.md](references/short-outline-spec.md)
- [references/consistency-check-spec.md](references/consistency-check-spec.md)
