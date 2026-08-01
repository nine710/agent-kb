# Extraction and Locator Rules

| Material | Preferred locator | Reliability | Fallback |
|---|---|---|---|
| Markdown | repository-relative path plus heading | high | line range when no heading exists |
| Code | repository-relative path plus symbol or line range | high | file path plus line range |
| HTML | canonical URL, title, anchor, and capture date | medium | extracted text heading |
| Text PDF | title, chapter/section, and page | medium | extracted text page marker |
| DOCX | heading and paragraph index | medium | extracted text heading |
| Scanned or damaged file | image/page marker only | low | request a readable source |

- Use installed environment tools for PDF or DOCX extraction. Do not add a project dependency merely to process one source.
- Record the tool, output path, source fingerprint, and reliability in `inventory.md`.
- `low` reliability claims may identify candidates but cannot independently support an Option, Tradeoff, application rule, or Anti-Pattern in a published card.
- A failed unit is `blocked`, not deleted. Continue with other units and record the failure in `progress.md` and the report.
