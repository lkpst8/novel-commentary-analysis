# HTML Output Specification

## Goal

Generate a standalone HTML page that makes the novel easy to understand at a glance while preserving real story structure and avoiding fabricated plot.

## Hard Requirements

- Output valid HTML, not markdown wrapped in code fences unless the user explicitly asks for fenced output.
- Use clear semantic headings.
- Keep section ordering stable so readers can scan quickly.
- Distinguish `原文明确` and `分析判断` when needed.
- Include a visible note when the source is partial or uncertain.
- Never invent missing scenes to make the HTML look complete.

## Required Page Structure

### 1. Header / Hero

Include:

- novel title
- one-sentence positioning
- source scope note
- spoiler note

Example content goals:

- 这是什么类型的故事
- 发生在怎样的环境里
- 读者接下来会看到什么维度的分析

### 2. Story Snapshot

Summarize the whole novel in 3 to 6 concise paragraphs or cards:

- 故事起点
- 核心矛盾
- 推进方式
- 故事落点

This section should answer “这本书到底讲了个什么故事”.

### 3. Background and World

Explain:

- time period
- location or space
- social/class/institutional setting
- world rules or operating logic

Possible labels:

- `时代背景`
- `空间环境`
- `制度规则`
- `世界运行逻辑`

### 4. Character Roster

Present major characters in a scan-friendly layout.

For each major character include:

- name
- role
- relation to the protagonist
- core drive
- key contradiction
- arc destination

### 5. Relationship Overview

Summarize the most important bonds and frictions:

- alliance
- romance
- family pressure
- rivalry
- power relationship
- betrayal or dependence

Do not list every minor contact. Only include relationships that materially affect story understanding.

### 6. Main Plot Timeline

This is the core section.

Break the main line into chronological stages such as:

- 开端
- 发展
- 升级
- 转折
- 崩塌/决断
- 结局

For each stage include:

- what happens
- why it matters
- what it triggers next

### 7. Major Subplots

For each important subplot include:

- subplot name
- involved characters
- what happens
- how it affects the main line or theme

If there are no clear major subplots in the available material, say so explicitly.

### 8. Key Turning Points

List the scenes or developments that most reshape the narrative.

For each turning point include:

- event
- immediate consequence
- long-tail impact

### 9. Ending and Aftermath

State clearly:

- how the central conflict lands
- what happens to major characters
- what remains unresolved
- what emotional tone the ending leaves

Do not dodge spoilers here unless the user requested spoiler-free output.

### 10. Themes and Emotional Core

Explain:

- dominant themes
- recurring pressures
- emotional pattern
- value conflict

Tie each theme back to story evidence.

### 11. Why the Novel Stays with Readers

Cover one or more of:

- character chemistry
- atmosphere
- pain or catharsis
- social texture
- dramatic structure
- memorable contradictions

### 12. Certainty and Source Notes

Always end with a compact note stating:

- whether the source was complete or partial
- where uncertainty exists
- whether any statements are interpretive rather than explicit

## Suggested HTML Skeleton

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>小说解读</title>
</head>
<body>
  <header>
    <h1>标题</h1>
    <p>一句话定位</p>
  </header>
  <main>
    <section id="snapshot">...</section>
    <section id="background-world">...</section>
    <section id="characters">...</section>
    <section id="relationships">...</section>
    <section id="main-plot">...</section>
    <section id="subplots">...</section>
    <section id="turning-points">...</section>
    <section id="ending">...</section>
    <section id="themes">...</section>
    <section id="memorability">...</section>
    <section id="source-notes">...</section>
  </main>
</body>
</html>
```

## Final Review Checklist

Before returning the HTML, check:

- Can a new reader understand the story without reading the novel?
- Are the people, world, and conflicts clearly separated?
- Is the main line chronological?
- Are subplots truly subplots rather than random incidents?
- Does every major claim trace back to the source?
- Did the draft accidentally invent connective tissue not present in the text?

If the answer to the last two questions is not a clear yes and no respectively, revise the page.
