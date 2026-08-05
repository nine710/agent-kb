# Material Profile Selection

Select one primary profile before creating a material package. Use `mixed` only when deliberately selected formats are complementary.

| Primary material boundary | Profile | Required version identity |
|---|---|---|
| Markdown or plain-text document files | `markdown-document-set` | file hashes or immutable repository commit |
| Human-provided local GitHub clone or repository snapshot | `github-repository` | human-provided repository URL and resolved commit |
| PDF or DOCX files | `pdf-docx` | file hashes and edition/version when available |
| Retained web pages or HTML snapshots | `web-archive` | canonical URL and capture date |
| Complementary units governed by more than one row above | `mixed` | explicit identity for every unit |

Declare each selected unit's profile in `inventory.md`. A clone, archive, or folder is a material container, not an automatic boundary. The manifest's `Material Boundary` table is the complete-reading set.

For duplicate representations, name the primary evidence representation and record the other representation as a cross-check. Do not count equivalent Markdown, HTML, PDF, or rendered content as independent support.
