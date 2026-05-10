---
name: novel-commentary-analysis
description: Analyze long novels with a token-efficient staged workflow and generate either complete HTML commentary pages or compressed plot outlines. Use when Codex needs to process full-length fiction from `.txt`, `.md`, `.html`, chapter dumps, multi-file novel folders, or pasted excerpts and output a structured analysis covering 人物, 背景, 世界观, 主线剧情, 支线剧情, 关键转折, 结局, 主题, or a short-form complete plot outline. Use especially when the source is very long and the work must stay faithful to the text without inventing scenes, motives, bridge events, settings, or endings.
---

# Novel Commentary Analysis

## 概览

用这个 skill 处理长篇小说时，不要反复把同一份原文重新喂给模型，而是先建立可复用的工作区，再基于中间产物继续分析和输出。

这个 skill 主要支持三种输出模式：

- `full-html`：完整 HTML 解读页
- `medium-outline`：中篇梗概版
- `short-outline`：短篇化完整剧情大纲

核心设计目标是节省 token。先把原文读入 workspace，然后优先消费 packet notes、phase summaries、各类 ledgers 和 compression artifacts，而不是每一步都回头重读整本小说。
注意：节省 token 不等于抽样读几个 packet。对长篇和超长篇来说，`medium-outline` 和 `short-outline` 必须建立在全量覆盖的 notes / ledgers / phase summaries 之上。
对于过长的梗概输出，也不要尝试一次性直接回答完；默认先分段写成多个本地 Markdown 文件，最后再合并。

## 模式选择

开始前先确定模式：

- `full-html`
  适合要输出完整 HTML 解读页的情况。目标是清楚说明这部小说讲了什么、谁重要、世界怎么运转、主线怎么推进、支线如何作用、结局怎么落地。

- `medium-outline`
  适合要一份比完整 HTML 更短、但仍然保留全书因果链的中篇梗概。

- `short-outline`
  适合把长篇或超长篇小说压缩成一份“短篇级完整故事骨架”。仍然要保留开场处境、诱发事件、升级、关键转折、结局和余韵。

如果用户没有明确指定模式，默认使用 `full-html`。

你可以直接按下面的中文方式理解和调用：

- `full-html`：生成完整 HTML 小说解读页
- `medium-outline`：生成中篇梗概
- `short-outline`：生成短篇化剧情大纲

## 不可妥协的忠实性规则

严格遵守以下规则：

- 不得虚构原文没有交代的情节、动机、设定、时间线、结果或人物关系。
- 不得为了让压缩更顺滑而补桥接事件。
- 不得把模糊暗示写成确定事实。
- 不得偷偷修正原文里本就混乱的时间顺序。
- 不得把次要支线拔高成主线。
- 如果原文不完整、抓取脏乱、OCR 受损，必须明确指出不确定性出现在哪里。
- 只要本地已经提供原文、节选、章节文件或现成 workspace，就不得去外部网站搜索小说大纲、剧情介绍、人物表或他人解读来代替分析。
- 外部搜索得到的梗概、书评、百科、论坛讨论，不得作为补全剧情的依据。
- 如果本地材料不足，只能明确标注 `材料不足`，不能用外部剧情摘要偷偷补齐。

需要时使用这些标签：

- `原文明确`
- `分析判断`
- `材料不足`

如果某个部分无法从现有材料中得出结论，也要保留这个部分，并写明：`原文材料不足，暂不下结论`。

## 反遗漏规则

对于超长篇小说，遗漏和脑补一样危险。

在输出最终结果前，至少确认：

- 每个 packet 都在 notes 或 ledgers 中被覆盖
- 每个 phase 都进入了最终的故事理解
- 每个关键人物都有明确作用和最终落点（如果原文支持）
- 每条关键支线都有起点、发展和收束状态（如果原文支持）
- 结局部分体现了后半段剧情，而不是只停留在前半段设定

如果这些问题回答不清楚，就不要定稿。

## 节省 Token 规则

这个 skill 的工作原则是：把原文当成“昂贵输入”，把 workspace 当成“可复用记忆层”。
这里的“可复用”前提是先把 coverage 做完整，而不是只抽样开头、中段、结尾几个 packet。

推荐顺序：

1. 原文只读一次，用来建立 workspace。
2. packet notes 只填一次。
3. 基于 notes 生成 ledgers。
4. 基于 ledgers 和 phase summaries 生成压缩稿。
5. 基于压缩稿和 ledgers 生成 HTML 或剧情大纲。

workspace 建好之后：

- 优先使用 `manifest.json`、`chapters.md`、packet notes、phase notes、ledgers、compression passes
- 只有在确实存在关键歧义时，才回头打开 raw packet
- 如果 workspace 里的中间产物已经覆盖需要的信息，不要重新从整本书开始总结

禁止把“节省 token”理解成：

- 只读第 1、60、120 个 packet 就写全书梗概
- 只抽开头、中段、结尾几个片段就生成 `medium-outline`
- 没完成 packet notes / phase notes / ledgers 就直接压缩成短纲

## 本地优先规则

这个 skill 必须坚持 `本地原文优先`：

1. 优先使用本地原文
2. 其次使用本地 workspace
3. 再其次使用本地生成的 notes / ledgers / compression passes

禁止行为：

- 已经有本地原文时，去网上搜“这本书讲了什么”
- 已经有 workspace 时，跳过 workspace 改去搜外部梗概
- 用百科、书评、论坛帖子、二手解读替代原文阅读

只有在下面这种情况才允许考虑外部信息，而且必须明确说明：

- 用户明确要求你对比外部版本、改编、出版信息或作者信息
- 用户根本没有提供文本，而任务本身又明确要求基于公开资料做概览

即使在这种特例下，也不能把外部梗概当成原文事实来输出。

## Python 运行规则

不要假设系统里存在 `python` 命令。

如果需要运行本 skill 自带脚本：

1. 先检查当前环境是否已有可用 Python。
2. 如果没有，就使用工作区依赖里提供的 bundled Python。
3. 不要因为 `python` 命令缺失就放弃脚本流程，更不要因此改去外部搜索剧情摘要。

在 Codex 桌面环境里，优先使用 `load_workspace_dependencies` 提供的 Python 路径。

## 输入判断

先识别：

- 输入类型：原始文件、多文件小说目录、节选，还是现成 workspace
- 目标模式：`full-html`、`medium-outline`、`short-outline`
- 覆盖范围：整本、某条人物线、某条关系线、某段剧情、某个主题
- 剧透要求：全剧透、有限剧透、无剧透
- 材料状态：完整、部分、不完整或受损

如果输入本身已经是带 `manifest.json` 的 workspace，就直接从 workspace 继续，不要重复建。

## 常规长度工作流

如果小说篇幅还没大到极易遗漏，可以使用这条流程：

1. 必要时先 packetize
2. 创建 packet notes
3. 建立 ledgers
4. 生成 compression passes
5. 生成目标输出
6. 跑 consistency checks

## 超长篇工作流

多 MB 到几十 MB 的小说，必须走分层流程：

1. 运行 `scripts/novel_packetizer.py`
2. 运行 `scripts/novel_chapter_detector.py`
3. 填写 `notes/packets/` 下的 packet notes
4. 填写 `notes/phases/` 下的 phase notes
5. 运行 `scripts/novel_ledger_builder.py`
6. 运行 `scripts/novel_outline_compressor.py`
7. 根据目标选择 `scripts/novel_html_builder.py` 或短纲 canon
8. 运行 `scripts/novel_consistency_checker.py`

超长篇不要跳过 note 和 ledger 层，这正是节省 token、避免反复重读原文的关键机制。
如果系统 `python` 不可用，就改用 bundled Python，不要改走外部搜索路线。

## `full-html` 规则

最终 HTML 应该让一个没看过书的人快速明白：

- 背景是什么
- 世界或制度逻辑是什么
- 主要人物是谁
- 关系结构是什么
- 主线在讲什么
- 重要支线在补充什么
- 哪些是关键转折
- 结局和余波是什么
- 主题和情绪核心是什么

除非用户明确缩小范围，否则至少包含：

1. 标题区
2. 故事速览
3. 背景与世界
4. 人物表
5. 人物关系概览
6. 主线剧情
7. 分阶段展开
8. 重要支线
9. 关键转折
10. 结局与余波
11. 主题与情绪核心
12. 来源与不确定性说明

对于超长篇，还建议加入：

- 快速目录导航
- 适合附录的溢出区
- 配角/阵营附录
- 详细时间线附录

参见 [references/html-output-spec.md](references/html-output-spec.md)

## `medium-outline` 规则

这个模式的目标是：在明显压缩篇幅的情况下，仍然保留完整主线因果链。

必须保留：

- 开场状态
- 诱发事件
- 升级过程
- 重大反转
- 结局
- 关键人物落点
- 对结局有影响的支线

可以压缩：

- 重复性的桥段
- 单纯氛围重复
- 不改变故事方向的小事件

这个模式应优先建立在 ledgers 和 full compression pass 之上，而不是重读整本原文。
对于长篇和超长篇，`medium-outline` 必须基于完整 packet coverage，而不能基于少量抽样 packet。
如果中篇梗概过长，默认流程是：

1. 先生成分段计划
2. 分段写入本地 Markdown 文件
3. 再合并为 `medium-outline.md`

## `short-outline` 规则

这个模式是把长篇重建成“短篇化完整故事骨架”。

仍然必须包含：

1. 开场处境
2. 诱发事件
3. 核心升级
4. 中段反转或重大转折
5. 后段大变化
6. 最终决断或对抗
7. 结局与余韵

推荐分阶段生成：

1. `compression-pass-1-full.md`
2. `compression-pass-2-medium.md`
3. `compression-pass-3-short.md`
4. `short-outline-canon.md`

如果最终短纲超出单次输出长度，就按 canon 分段输出，不要靠上下文记忆续写。
对于长篇和超长篇，`short-outline` 必须建立在完整覆盖后的 compression chain 上，不能靠少量 packet 抽样拼接。
默认做法不是直接把最终短纲一次性输出给用户，而是：

1. 先按 canon 规划多段
2. 每段单独写入本地 Markdown 文件
3. 最后合并成总稿

参见 [references/short-outline-spec.md](references/short-outline-spec.md)

## 输出前检查

输出前至少确认：

- 没有新增原文不存在的情节或动机
- 主线和支线没有混淆
- 结局与已知原文一致
- 后半段没有因为压缩而消失
- 每个 phase 都在最终理解里被代表
- 能用 workspace 中间产物解决的问题，就不要重复重读原文

如果这些检查不通过，先修正再返回。

## 工具与参考

脚本：

- `scripts/novel_packetizer.py`
- `scripts/novel_chapter_detector.py`
- `scripts/novel_ledger_builder.py`
- `scripts/novel_outline_compressor.py`
- `scripts/novel_outline_segmenter.py`
- `scripts/novel_outline_merger.py`
- `scripts/novel_html_builder.py`
- `scripts/novel_consistency_checker.py`

运行脚本时：

- 优先用当前环境可用的 Python
- 若不可用，则使用 bundled Python
- 不要把“无法直接运行 python”当成改用外部剧情网站的理由

参考：

- [references/commentary-framework.md](references/commentary-framework.md)
- [references/html-output-spec.md](references/html-output-spec.md)
- [references/large-novel-scaling.md](references/large-novel-scaling.md)
- [references/ledger-spec.md](references/ledger-spec.md)
- [references/short-outline-spec.md](references/short-outline-spec.md)
- [references/consistency-check-spec.md](references/consistency-check-spec.md)
