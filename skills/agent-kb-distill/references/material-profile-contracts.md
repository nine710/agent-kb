# Material Profile Contracts

## Markdown Document Set

Inventory one row per included file and read every included file. Locate claims with repository-relative path plus heading; use a line range only when a stable heading is unavailable. Rendered duplicates are cross-checks, not replacements for selected Markdown.

## GitHub Repository

A human-provided local clone is immutable upstream material. Do not run Git commands, fetch, pull, change branches, or modify it. The human supplies the repository URL and resolved commit. The manifest declares included paths, exclusions, and reasons; the clone itself is never the reading boundary.

Inventory documentation, implementation, tests, examples, generated material, binaries, metadata, and auxiliary material separately. Locate code with path plus symbol or line range plus commit. Documentation states intent and contracts; implementation demonstrates available behavior; tests demonstrate asserted behavior, not unstated architectural intent. Mark a clone with local changes `human-modified`; it is not publishable until the human separates the overlay from the upstream boundary and supplies an `upstream-clean` snapshot.

## PDF And DOCX

Inventory each file and use page or section subunits when needed for progress. Record the extraction tool, output, and quality check. Use title, section/chapter, and page for PDF; add heading and paragraph index for DOCX. Visually cross-check tables, diagrams, code samples, and layout-dependent statements. OCR-only, scanned, or damaged text is low reliability and cannot independently support a published field.

## Web Archive

Inventory each retained page. Locate claims with canonical URL, title, anchor or heading, capture date, and retained snapshot. Treat changing, client-rendered, or inaccessible content as medium reliability unless an immutable upstream representation exists. Prefer the selected Markdown or repository source when it represents the same material.

## Mixed Package

Use mixed only when the formats are complementary. Every inventory unit names its governing profile, and the manifest explains the role of each format. Assign a primary representation for duplicate content and retain the duplicate only as a cross-check. Preserve conflicts between representations rather than using duplicate formats to manufacture consensus.
