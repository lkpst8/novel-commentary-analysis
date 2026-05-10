---
name: novel-commentary-analysis
description: Analyze long novels and generate complete HTML commentary pages that let readers quickly understand what story the novel tells. Use when Codex needs to read or process full-length fiction from `.txt`, `.md`, `.html`, chapter dumps, or pasted excerpts and output a structured novel briefing covering 人物, 背景, 世界观, 主线剧情, 支线剧情, 关键转折, 结局, 主题, and reading value. Use especially when the output must be clear, navigable, visually structured, and strictly faithful to the source text without inventing scenes, motives, settings, or plot developments.
---

# Novel Commentary Analysis

## Overview

Read long-form fiction and convert it into a standalone HTML analysis page that helps the user quickly understand what the novel is about. Keep the output source-faithful, highly structured, spoiler-aware when requested, and explicit about what is directly supported by the text versus what is interpretive synthesis.

## Default Deliverable

Default to a full HTML page unless the user explicitly asks for another format.

The HTML deliverable should help a reader answer these questions quickly:

- 这部小说发生在什么背景里
- 这个世界是怎么运转的
- 主要人物是谁，他们彼此是什么关系
- 故事的主线到底在讲什么
- 重要支线在补充什么
- 剧情是如何一步步推进到结局的
- 这部小说最核心的主题、情绪和记忆点是什么

When the user only provides a partial excerpt, still use the HTML structure, but clearly mark the page as `基于节选分析` and avoid pretending to summarize the full novel.

## Non-Negotiable Fidelity Rules

Strictly obey these rules:

- Do not invent scenes, motives, settings, timelines, outcomes, or relationships that are not supported by the source.
- Do not fill gaps with “likely” events unless they are clearly labeled as uncertainty.
- Do not merge separate characters or reorder events without saying so.
- Do not exaggerate the importance of a side plot just to make the page look fuller.
- If the text is incomplete, OCR-damaged, or packetized from messy input, say exactly where certainty drops.
- If you infer subtext, mark it as `分析判断` rather than `原文明确交代`.

If a requested section cannot be filled from the available material, keep the section and say `原文材料不足，暂不下结论`.

## Intake

Identify the scope before writing:

- Source type: full book, chapter subset, packetized text, excerpt, or HTML summary.
- Coverage: whole novel, one arc, one character line, one relationship line, or one theme.
- Spoiler level: full spoilers, limited spoilers, or spoiler-free.
- Delivery goal: reading guide,解说稿底稿, video/article page, archive page, or study notes.
- Certainty level: complete source, partial source, or damaged source.

If the novel is too long for a reliable single-pass read, run `scripts/novel_packetizer.py` first and synthesize from the generated workspace rather than from a single raw file.

## Reading Model

Build the analysis around these core layers:

- `背景`
  Capture era, geography, class environment, institutional setting, family structure, or survival conditions.

- `世界观`
  Explain the rules of the story world. This can mean political order, military system, cultivation rules, workplace order, social hierarchy, or emotional code.

- `人物`
  Identify protagonist, major supporting cast, antagonistic pressure, relational mirrors, and emotional anchors.

- `主线剧情`
  Explain the central conflict from setup to ending in chronological order.

- `支线剧情`
  Track side arcs that deepen theme, reshape relationships, or redirect the main line.

- `结构转折`
  Mark opening hook, first decisive turn, mid-story escalation, collapse/reversal, late revelation, and ending residue.

- `主题与气质`
  Extract what the novel repeatedly expresses through scenes, choices, institutions, and emotional patterns.

## Very Long Novel Mode

Use this mode for novels that are multiple megabytes long or large enough that a single-pass summary would almost certainly miss characters, subplots, or major turns.

Process the source hierarchically:

1. Split the source into `packets/`.
2. Group packets into `phases/`.
3. Track every packet in `coverage-ledger.md`.
4. Build rolling notes for characters, worldbuilding, factions, relationships, main-line stages, and subplot states.
5. Only after phase-level synthesis, draft the final HTML.

Never jump directly from a tens-of-megabytes source file to a one-shot summary. That is how main plot beats, secondary arcs, and late-introduced characters get lost.

For very long novels, every packet should be represented in at least one of these final destinations:

- main plot timeline
- subplot section
- character update
- world/background note
- certainty/source note

## Required HTML Sections

Unless the user narrows the task, include all of these sections in the HTML output:

1. Title block
2. Story snapshot
3. Background and world
4. Character roster
5. Relationship overview
6. Main plot timeline
7. Major subplots
8. Key turning points
9. Ending and aftermath
10. Themes and emotional core
11. Why the novel is memorable
12. Certainty and source notes

For very long novels, also add:

13. Quick navigation table of contents
14. Phase-by-phase or act-by-act breakdown
15. Extended supporting cast or faction appendix when needed
16. Subplot index showing where each subplot begins, escalates, and resolves

You may add sections like `叙事视角`, `阵营结构`, `时间线`, `名场面`, or `改编提示` when the source supports them.

Read [references/html-output-spec.md](references/html-output-spec.md) for the detailed structure and section-level requirements before drafting.

## Section Writing Rules

Apply these rules while filling the HTML page:

- `故事速览` should let a new reader understand the book in under one minute.
- `背景与世界观` should explain the operating environment, not just decorate the page.
- `人物` should focus on role, motive, pressure, and arc, not empty adjectives.
- `主线剧情` must follow chronology and causality.
- `支线剧情` should explain how each subplot affects the main line, theme, or character development.
- `结局` should state what actually happens and what emotional/structural consequences remain.
- `主题` should come from repeated evidence, not a slogan pasted on top of the story.

For very long novels, keep two levels of explanation:

- `速览层`: a compressed explanation for readers who want the whole story fast
- `展开层`: detailed sections that preserve the important progression of plot, people, and subplots

If the page becomes long, compress phrasing before deleting events. Prefer using anchor navigation, `details/summary`, appendices, and phase sections rather than dropping material.

## Output Method

When producing the final HTML:

1. Extract notes first.
2. Build a clean chronology.
3. Separate main line from side line.
4. Group characters by dramatic function.
5. Draft the HTML using the required sections.
6. Run a final fidelity pass and remove anything not grounded in the source.

Prefer semantic HTML with clear headings, summary cards, and compact section intros. Keep the layout easy to scan on desktop and mobile. Inline CSS is acceptable if the user asks for a standalone file.

For very long novels, the HTML should be multi-layered:

- top-level quick answer section
- navigable table of contents
- concise character and world summary near the top
- main plot broken into phases or acts
- subplot cards or grouped sections
- optional appendices for extended cast, faction notes, or detailed chronology

## Fidelity Check Before Finalizing

Before you present the output, verify:

- Every major plot claim comes from the source or a clearly marked inference.
- No invented bridge scenes were added between known events.
- Character motives are not overstated beyond textual support.
- Main plot and subplots are not confused.
- The ending section matches the provided material.
- Uncertainty is visible wherever the source is incomplete.

If any item fails, fix the draft before returning it.

## Tools and References

Use [references/commentary-framework.md](references/commentary-framework.md) for the long-form reading method.

Use [references/html-output-spec.md](references/html-output-spec.md) for the exact HTML page structure and content contract.

Use [references/large-novel-scaling.md](references/large-novel-scaling.md) when the source is large enough that omission risk becomes the main problem.

If needed, packetize long source text:

```bash
python scripts/novel_packetizer.py input.txt output_dir --title "Book Title" --max-chars 10000 --packets-per-phase 6
```

The script generates:

- `packets/` for low-level reading
- `phases/` for mid-level synthesis
- `coverage-ledger.md` to prevent silent omissions
- `html-outline-template.md` to structure long HTML output
- `manifest.json` for machine-readable workspace metadata

Then analyze packet by packet, merge notes phase by phase, and only after that write the final HTML page.
