# Source Intake Rules

1. Scan `raw/sources.md` and `raw/src-*/` for existing `src-NNN` IDs. Assign the highest ID plus one only when no existing source has the same official URL, repository URL, or material fingerprint.
2. Normalize the source slug to lowercase kebab-case. Create `raw/src-NNN-<slug>/{source,derived,excerpts}`.
3. Add the public source metadata to `raw/sources.md`: ID, title, author or organization, URL, license, format, local package path, and primary locator strategy.
4. Copy or clone only human-selected materials into `source/`. Keep the upstream organization intact.
5. If a URL, repository, or fingerprint matches an existing source, reuse its ID and package. Do not create a duplicate source package.
6. Record unavailable licenses, inaccessible URLs, or missing primary material in `manifest.md` as `blocked`; do not publish cards from blocked material.
