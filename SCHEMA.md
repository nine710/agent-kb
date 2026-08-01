# SCHEMA.md — agent-kb 卡片规范

## 卡片文件

卡片是 `cards/` 目录下的 markdown 文件，文件名 = `id.md`。

## Frontmatter

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | kebab-case，全库唯一，等于文件名（不含 .md） |
| `problem` | string | 是 | 一句话设计决策问题（可反复遇到，不绑定单篇文章） |
| `tags` | string[] | 是 | 主题标签（如 harness, constitution, hooks） |
| `when_to_use` | string | 是 | 什么场景下会遇到此问题 |
| `when_not` | string | 是 | 什么场景不适用 |
| `status` | string | 是 | `draft`（草稿）/ `active`（正式）/ `deprecated`（废弃） |
| `source_ids` | string[] | 是 | 关联 `raw/sources.md` 中的源 ID |

## 正文章节

| 章节 | 必填 | 硬约束 |
|------|------|--------|
| **Options** | 是 | ≥3 个真分歧选项；每个选项有名称和描述 |
| **Tradeoffs** | 是 | 每个选项的优势与代价 |
| **Apply to Agent Development** | 是 | 外部可推导的通用决策规则；禁止个人项目经验 |
| **Anti-Patterns** | 是 | 源中或逻辑可证的反模式；禁止个人经验 |
| **Sources** | 是 | 每条含源 ID + 源原生稳定定位（Markdown 标题优先；其他格式用可复核页码、锚点或文件位置） |

## 硬约束

1. **≥3 真选项**：不是同一方案的变体，是真正不同的设计路径
2. **零个人经验**：所有字段不含个人项目经历（项目名、踩坑记录等）
3. **源可追溯**：每个选项、tradeoff、应用规则都能回溯到 sources
4. **problem 可复用**：是设计问题模板，不是文章读后感

## 对抗审查清单（草稿进 cards/ 前必检）

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 真三叉 | options ≥3 且是不同方案路径 |
| 2 | 非摘要 | 是决策单元，不是文章摘要 |
| 3 | 零个人经验 | 无任何个人项目经历 |
| 4 | 源可追溯 | 每条内容可回溯到 sources |
| 5 | problem 可复用 | 可反复遇到的设计问题 |

## raw/ 原材料与摘录规范

- `raw/sources.md`：公开，必读源索引
- `raw/src-NNN-<source-slug>/`：每个来源的本地材料包，由 `.gitignore` 排除
- `raw/src-NNN-<source-slug>/source/`：不修改的上游原始材料；项目、配套文件、PDF 或文档属于同一来源时放在同一个材料包中
- `raw/src-NNN-<source-slug>/derived/`：Agent 生成的材料画像、提取文本、证据台账、候选问题、进度和蒸馏报告
- `raw/src-NNN-<source-slug>/excerpts/`：该来源的 fair-use 短摘录和定位笔记
- 摘录长度上限：单条不超过 500 字，单源摘录总计不超过 2000 字
- 每条摘录必须标注精确来源定位（优先 Markdown 章节 / 小节；其他格式使用源原生稳定定位）
- `excerpts/` 不复制来源全文、整书 PDF 或 EPUB；原始材料可原样保留在同一材料包的 `source/` 中，但材料包不进入公开仓库

## 源材料格式优先级

1. markdown 源码（首选）
2. GitHub 网页（可用）
3. PDF（备选）
4. EPUB（不用）
