#!/usr/bin/env python3
"""Validate source-level distillation artifacts before card publication."""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_DERIVED = (
    "manifest.md",
    "inventory.md",
    "progress.md",
    "evidence-ledger.md",
    "candidate-problems.md",
    "distillation-report.md",
)
CLAIM_ID_RE = re.compile(r"\bCLM-\d+\b")
KEY_VALUE_RE = re.compile(r"^(?:-\s*)?([a-z_]+):\s*(.+)$", re.MULTILINE)


def read_markdown_table(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("|") or index + 1 >= len(lines):
            continue
        separator = lines[index + 1]
        if not separator.startswith("|") or "---" not in separator:
            continue
        headers = [cell.strip() for cell in line.strip("|").split("|")]
        rows = []
        for row_line in lines[index + 2 :]:
            if not row_line.startswith("|"):
                break
            values = [cell.strip() for cell in row_line.strip("|").split("|")]
            if len(values) != len(headers):
                continue
            rows.append(dict(zip(headers, values)))
        return rows
    return []


VALID_DRAFT_STATUSES = {"draft", "published", "raw-only", "out-of-scope", "rejected"}


def draft_files(drafts_dir, source_id):
    source_drafts = Path(drafts_dir) / source_id
    if not source_drafts.exists():
        return []
    return sorted(
        path
        for path in source_drafts.rglob("*.md")
        if path.is_file() and not path.name.endswith(".evidence.md")
    )


def evidence_files(drafts_dir, source_id):
    source_drafts = Path(drafts_dir) / source_id
    if not source_drafts.exists():
        return []
    return sorted(
        path
        for path in source_drafts.rglob("*.evidence.md")
        if path.is_file()
    )


def metadata(text):
    return {key: value.strip() for key, value in KEY_VALUE_RE.findall(text)}


def candidate_records(path):
    records = {}
    current_id = None
    current_lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current_id:
                records[current_id] = metadata("\n".join(current_lines))
            current_id = line[3:].strip()
            current_lines = []
        elif current_id:
            current_lines.append(line)
    if current_id:
        records[current_id] = metadata("\n".join(current_lines))
    return records


def sidecar_bindings(path):
    text = path.read_text(encoding="utf-8")
    bindings = []
    for line in text.splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label, claim_text = line[2:].split(":", 1)
        bindings.append((label.strip(), sorted(set(CLAIM_ID_RE.findall(claim_text)))))
    return metadata(text), bindings


def frontmatter_value(path, key):
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def published_card_path(value, cards_dir):
    if not value:
        return None
    target = Path(value)
    if target.suffix != ".md":
        target = target.with_suffix(".md")
    if not target.is_absolute():
        cards_dir = Path(cards_dir)
        if target.parts and target.parts[0] == cards_dir.name:
            target = cards_dir.parent / target
        else:
            target = cards_dir / target
    return target


def validate_draft_lifecycle(draft, draft_metadata, candidate, cards_dir):
    errors = []
    status = draft_metadata.get("status", "")
    published_card = draft_metadata.get("published_card", "")
    decision_reason = draft_metadata.get("decision_reason", "")
    candidate_id = draft_metadata.get("candidate_id", "")

    if status not in VALID_DRAFT_STATUSES:
        errors.append(f"unknown draft status for {draft.name}: {status or '<empty>'}")
        return errors

    if status == "published":
        if not published_card:
            errors.append(f"published draft must set published_card: {draft.name}")
        else:
            card = published_card_path(published_card, cards_dir)
            if not card.is_file():
                errors.append(f"published card does not exist for {candidate_id}: {published_card}")
            elif frontmatter_value(card, "status") != "active":
                errors.append(f"published card must have active status: {card.name}")
    elif published_card:
        errors.append(f"non-published draft must not set published_card: {draft.name}")

    if status in {"raw-only", "out-of-scope", "rejected"} and not decision_reason:
        errors.append(f"{status} draft must include decision_reason: {draft.name}")

    if status == "raw-only" and candidate.get("three_way_assessment") == "pass":
        errors.append(f"raw-only candidate must not have three_way_assessment: pass: {candidate_id}")

    candidate_status = candidate.get("status", "")
    terminal_statuses = {"raw-only", "out-of-scope", "rejected"}
    if candidate_status in terminal_statuses and status != candidate_status:
        errors.append(
            f"draft status must match candidate status for {candidate_id}: "
            f"{candidate_status} requires {candidate_status}, got {status}"
        )

    return errors


def validate_package(package_root, drafts_dir, cards_dir):
    package_root = Path(package_root)
    drafts_dir = Path(drafts_dir)
    cards_dir = Path(cards_dir)
    errors = []
    derived = package_root / "derived"

    for filename in REQUIRED_DERIVED:
        if not (derived / filename).is_file():
            errors.append(f"missing derived artifact: {derived / filename}")

    if errors:
        return errors

    source_id = metadata((derived / "manifest.md").read_text(encoding="utf-8")).get("source_id", "")
    if not source_id:
        errors.append("manifest.md must include source_id")

    progress_text = (derived / "progress.md").read_text(encoding="utf-8")
    if "stage:" not in progress_text or "last_locator:" not in progress_text:
        errors.append("progress.md must include stage and last_locator")

    candidates = candidate_records(derived / "candidate-problems.md")
    if not candidates:
        errors.append("candidate-problems.md must include status and three_way_assessment")

    claims = {
        row.get("claim_id"): row
        for row in read_markdown_table(derived / "evidence-ledger.md")
        if row.get("claim_id")
    }
    if not claims:
        errors.append("evidence-ledger.md must contain a claim table")

    source_drafts = draft_files(drafts_dir, source_id)
    source_evidence = evidence_files(drafts_dir, source_id)
    source_draft_stems = {path.stem for path in source_drafts}
    source_evidence_stems = {path.name[: -len(".evidence.md")] for path in source_evidence}
    for orphan in sorted(source_evidence_stems - source_draft_stems):
        errors.append(f"orphan evidence sidecar: {orphan}.evidence.md")
    for path in sorted(Path(drafts_dir).glob("*.md")):
        errors.append(f"unscoped draft archive outside {source_id}: {path.name}")
    for path in sorted(Path(drafts_dir).glob("*.evidence.md")):
        errors.append(f"unscoped evidence sidecar outside {source_id}: {path.name}")

    candidate_drafts = {}
    for draft in source_drafts:
        draft_metadata = metadata(draft.read_text(encoding="utf-8"))
        draft_source_id = draft_metadata.get("source_id", "")
        if draft_source_id != source_id:
            errors.append(f"{draft.name} must declare source_id: {source_id}")
            continue
        candidate_id = draft_metadata.get("candidate_id", "")
        if not candidate_id:
            errors.append(f"draft must declare candidate_id: {draft.name}")
            continue
        candidate_drafts.setdefault(candidate_id, []).append(draft)
        candidate = candidates.get(candidate_id)
        if candidate is None:
            errors.append(f"draft references missing candidate: {candidate_id}")
            continue
        sidecar = draft.with_name(f"{draft.stem}.evidence.md")
        if not sidecar.is_file():
            errors.append(f"missing evidence sidecar: {sidecar.name}")
            continue
        sidecar_metadata, bindings = sidecar_bindings(sidecar)
        if sidecar_metadata.get("source_id") != source_id:
            errors.append(f"{sidecar.name} must declare source_id: {source_id}")
            continue
        if sidecar_metadata.get("candidate_id") != candidate_id:
            errors.append(f"{sidecar.name} candidate_id does not match draft: {candidate_id}")
            continue
        errors.extend(validate_draft_lifecycle(draft, draft_metadata, candidate, cards_dir))
        if not bindings or not any(claim_ids for _, claim_ids in bindings):
            errors.append(f"evidence sidecar has no claim IDs: {sidecar.name}")
            continue
        for label, claim_ids in bindings:
            for claim_id in claim_ids:
                claim = claims.get(claim_id)
                if claim is None:
                    errors.append(f"{sidecar.name} references missing claim: {claim_id}")
                    continue
                status = claim.get("support_status", "")
                if label.lower().startswith("option") and status != "supported":
                    errors.append(f"{sidecar.name} {label} must use supported claim: {claim_id}")
                if status in {"unsupported", "conflict"}:
                    errors.append(f"{sidecar.name} references {status} claim: {claim_id}")
                if claim.get("reliability", "") == "low":
                    errors.append(f"{sidecar.name} references low-reliability claim: {claim_id}")
                if status == "inferred" and not claim.get("inference_chain", ""):
                    errors.append(f"inferred claim lacks inference_chain: {claim_id}")

    for candidate_id in candidates:
        matching = candidate_drafts.get(candidate_id, [])
        if not matching:
            errors.append(f"missing draft archive for candidate: {candidate_id}")
        elif len(matching) > 1:
            errors.append(f"duplicate candidate_id in draft archives: {candidate_id}")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_package", type=Path)
    parser.add_argument("--drafts", type=Path, required=True)
    parser.add_argument("--cards", type=Path, required=True)
    args = parser.parse_args()

    errors = validate_package(args.source_package, args.drafts, args.cards)
    if errors:
        print(f"FAIL: {args.source_package}")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1
    print(f"PASS: {args.source_package}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
