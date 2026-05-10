---
name: novel-commentary-analysis
description: Analyze long novels and turn them into structured commentary, recap, and interpretation outputs. Use when Codex needs to read or process full-length fiction from `.txt`, `.md`, `.html`, chapter dumps, or pasted excerpts and produce plot梳理, 人物弧光分析, 主题提炼, 关系网整理, 分集/分章节解说大纲, or long-form narration plans for video, article, or oral commentary.
---

# Novel Commentary Analysis

## Overview

Build a reusable workflow for reading long novels and converting them into clear, evidence-based commentary outputs. Keep the work grounded in the source text, separate direct textual support from inference, and prefer structured intermediate notes before writing the final解说稿.

## Workflow Decision

Choose the output mode before drafting:

- Use `剧情梳理` when the user mainly needs chronological recap and causality.
- Use `人物分析` when the request centers on motives, growth, contradiction, and relationships.
- Use `主题解读` when the request asks what the novel is “really about” and how it expresses its时代气质, 阶层关系, 情感结构, or价值冲突.
- Use `解说脚本` when the user wants a narrator-ready long-form output for article, video, podcast, or直播.
- Use `拆书方案` when the user wants serial content such as “10期讲完一本书”.

If the request is ambiguous, default to this sequence:
1. Plot skeleton
2. Character arc map
3. Theme and emotional core
4. Final commentary format requested by the user

## Intake

Start by identifying:

- Source format: full text, excerpt, chapter list, HTML page, or prior notes.
- Coverage target: full book, selected arc, single character, single relationship line, or one theme.
- Spoiler policy: full spoilers allowed, limited spoilers, or spoiler-free recommendation.
- Delivery target: summary notes, article outline, video script, episode plan, or polished prose.
- Evidence standard: whether the user wants close reading with citations or a broader interpretive read.

If the input is longer than the model can comfortably reason over in one pass, run `scripts/novel_packetizer.py` first to generate packetized markdown files and an index. Then analyze packet by packet before synthesizing the whole.

## Build the Reading Model

Extract these anchors early:

- Story frame: setting, era, class environment, narrative voice, POV stability.
- Main conflict: what each major figure wants, what blocks them, and what the cost of failure is.
- Plot engines: secrets, misrecognitions, reversals, institutions, family structures, war/industry/official systems, romance, revenge, survival.
- Emotional spine: longing, resentment, shame, loyalty, rivalry, tenderness, ambition, sacrifice.
- Structural pivots: opening hook, first irreversible turn, mid-story escalation, collapse point, late revelation, ending aftertaste.

Record notes in a compact matrix. For each major character or line, keep:

- `surface role`
- `hidden drive`
- `turning point`
- `relationship pressure`
- `ending state`

## Analyze Before Writing

Build the commentary from at least four layers:

1. `What happens`
Chronological plot and causality. Explain not only events but why each event triggers the next.

2. `Who changes`
Track character motion. Note who grows, who hardens, who breaks, who remains trapped, and what forces that outcome.

3. `What it means`
Identify recurring images, class positions, institutions, speech habits, or emotional patterns that support the theme.

4. `Why it works`
Explain the narrative pleasure: momentum, reversals, chemistry, atmosphere, realism, cruelty, wish-fulfillment, tragedy, or moral tension.

Avoid jumping to the final “theme” too early. Earn interpretation from observed details.

## Draft the Output

Use an output shape that fits the request.

For `剧情梳理`, prefer:
- One-paragraph premise
- Chronological stages
- Cause-and-effect transitions
- Ending and aftermath
- One short interpretation paragraph

For `人物分析`, prefer:
- Character baseline
- Desire and fear
- Key relationships
- Three decisive turns
- Final arc judgment

For `主题解说` or `长篇解说稿`, prefer:
- Hook
- Premise and world
- Major plot stages
- Character and relationship pressure
- Theme extraction
- Why readers remember it
- Closing takeaway

When the user wants a serial script, break the whole book into episodes by stable dramatic units rather than equal chapter counts. Each episode should end on a hook, reversal, reveal, or emotional cliff.

## Quality Bar

Keep these guardrails:

- Do not fabricate scenes or motives not supported by the source. Mark uncertain inference explicitly.
- Distinguish `text-supported` conclusions from `interpretive` conclusions.
- Preserve chronology. If you reorder for effect, say so.
- Do not flatten morally mixed characters into single labels.
- For adaptation-oriented commentary, note what is omitted, compressed, or heightened.
- If the source text is messy OCR or an incomplete scrape, say where the uncertainty comes from.

## References and Tools

Read [references/commentary-framework.md](references/commentary-framework.md) when you need the detailed analysis framework, reusable templates, or episode planning heuristics.

Run the packetizer when the novel is too long for a single-pass reading workflow:

```bash
python scripts/novel_packetizer.py input.txt output_dir --title "Book Title"
```

The script creates:

- `index.md` with packet overview
- `packet-001.md`, `packet-002.md`, ... for staged reading

Use those packets to produce intermediate notes first, then synthesize the final commentary.
