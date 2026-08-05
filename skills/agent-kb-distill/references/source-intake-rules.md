# Source Intake Rules

1. Scan `raw/sources.md` and `raw/src-*/` for existing `src-NNN` IDs. Assign the highest ID plus one only when no existing source has the same official URL, repository URL, or material fingerprint.
2. Normalize the source slug to lowercase kebab-case. Create `raw/src-NNN-<slug>/{source,derived,excerpts}`.
3. Add the public source metadata to `raw/sources.md`: ID, title, author or organization, URL, license, format, local package path, and primary locator strategy.
4. Read [material profile selection](material-profile-selection.md). For every new or re-distilled package, write `material_contract_version: v1`, select the primary profile, and declare `snapshot`, `provenance`, `material_state`, profile references, and a finite `Material Boundary` table before reading.
5. Copy only human-selected materials into `source/`. For a human-provided local GitHub clone, do not run Git commands, change branches, fetch, pull, or modify the clone. Record the human-provided repository URL and resolved commit in the manifest.
6. The boundary table, not the source container, defines the complete-reading obligation. Record each included root/path and each exclusion/pattern with its reason. Inventory excluded and unreadable units rather than deleting them from the audit trail.
7. If a URL, repository, or fingerprint matches an existing source, reuse its ID and package. Do not create a duplicate source package.
8. Record unavailable licenses, inaccessible URLs, missing primary material, unresolved snapshot identity, or an unusable material state as `blocked`; do not publish cards from blocked material.
