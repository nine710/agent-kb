# agent-kb

AI Agent 设计知识库：策展决策卡（curated decision cards），用于提升编程智能体在设计阶段的设计上限。

## 这是什么

不是论文全文库，而是**决策卡**——每张卡是一个可反复遇到的设计问题，附带 ≥3 个真选项、tradeoffs、应用规则和来源。

## 怎么用

1. 在设计/brainstorm 时，按问题关键词翻 `cards/` 下的卡片
2. 每张卡提供多个真实方案分叉，帮助看到更多可能性
3. `raw/sources.md` 列出全部源材料索引

## 卡片结构

详见 `SCHEMA.md`。空白模板见 `templates/card.md`。

## 本地蒸馏材料

`raw/` 是蒸馏输入层。`raw/sources.md` 是公开的来源索引；每个实际来源的原始文件、配套项目和 fair-use 摘录都收纳在同一个本地材料包中：`raw/src-NNN-<source-slug>/source/` 与 `raw/src-NNN-<source-slug>/excerpts/`。材料包由 `.gitignore` 排除，不进入公开仓库。

## 验证

```bash
python scripts/validate_card.py --all   # 验证所有正式卡
```

## 许可

卡片内容（`cards/`）基于 Apache 2.0 源材料蒸馏。源材料许可各自独立，见 `raw/sources.md`。
