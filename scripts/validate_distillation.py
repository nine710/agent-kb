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


def draft_files(drafts_dir):
    if not drafts_dir.exists():
        return []
    return sorted(
        path
        for path in drafts_dir.glob("*.md")
        if not path.name.endswith(".evidence.md")
    )


def metadata(text):
    return {key: value.strip() for key, value in KEY_VALUE_RE.findall(text)}


def card_source_ids(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^source_ids:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


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

    for draft in draft_files(drafts_dir):
        if source_id not in card_source_ids(draft):
            continue
        sidecar = draft.with_name(f"{draft.stem}.evidence.md")
        if not sidecar.is_file():
            errors.append(f"missing evidence sidecar: {sidecar.name}")
            continue
        sidecar_metadata, bindings = sidecar_bindings(sidecar)
        if sidecar_metadata.get("source_id") != source_id:
            errors.append(f"{sidecar.name} must declare source_id: {source_id}")
            continue
        candidate_id = sidecar_metadata.get("candidate_id", "")
        candidate = candidates.get(candidate_id)
        if candidate is None:
            errors.append(f"{sidecar.name} references missing candidate: {candidate_id or '<empty>'}")
            continue
        if candidate.get("status") != "new":
            errors.append(f"{sidecar.name} references non-publishable candidate {candidate_id}: {candidate.get('status', '<empty>')}")
        if candidate.get("three_way_assessment") != "pass":
            errors.append(f"{sidecar.name} candidate {candidate_id} lacks three_way_assessment: pass")
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

        published = cards_dir / draft.name
        if published.is_file() and frontmatter_value(published, "status") != "active":
            errors.append(f"published card must have active status: {published.name}")

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
