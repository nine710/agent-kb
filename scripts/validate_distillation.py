#!/usr/bin/env python3
"""Validate source-level distillation artifacts before card publication."""

import argparse
import importlib.util
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
    "decision-map-alignment.md",
    "map-change-proposals.md",
    "card-review.md",
)
CLAIM_REF_RE = re.compile(r"\bsrc-\d{3}/CLM-\d+\b|\bCLM-\d+\b")
REVIEW_REF_RE = re.compile(r"\bXSR-\d+\b")
KEY_VALUE_RE = re.compile(r"^(?:-[ \t]*)?([a-z_]+):[ \t]*(.+)$", re.MULTILINE)


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


def read_markdown_table_after_heading(path, heading):
    lines = path.read_text(encoding="utf-8").splitlines()
    for heading_index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        for index in range(heading_index + 1, len(lines)):
            line = lines[index]
            if line.startswith("## "):
                break
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


def claim_refs(text):
    return sorted(set(CLAIM_REF_RE.findall(text or "")))


VALID_DRAFT_STATUSES = {"draft", "published", "raw-only", "out-of-scope", "rejected"}
DEVELOPMENT_AGENT_CONTRACT = "development-agent-v1"
MATERIAL_CONTRACT_VERSION = "v1"
VALID_MATERIAL_PROFILES = {
    "markdown-document-set",
    "github-repository",
    "pdf-docx",
    "web-archive",
    "mixed",
}
VALID_MATERIAL_STATES = {"upstream-clean", "human-modified", "unknown", "blocked"}
VALID_CONTENT_ROLES = {
    "documentation",
    "implementation",
    "test",
    "example",
    "generated",
    "binary",
    "metadata",
    "auxiliary",
}
VALID_SOURCE_POSITIONS = {"primary", "corroborating", "auxiliary"}
VALID_CONFLICT_STATUSES = {
    "none",
    "version-drift",
    "distinct-scope",
    "documentation-defect",
    "test-implementation-mismatch",
    "unresolved",
}
VALID_CROSS_SOURCE_STATUSES = {
    "consistent",
    "distinct-scope",
    "superseded",
    "unresolved",
    "no-overlap",
}
REQUIRED_MATERIAL_FIELDS = (
    "material_profile",
    "source_boundary",
    "snapshot",
    "provenance",
    "material_state",
    "profile_refs",
    "input_fingerprint",
)
REQUIRED_INCLUDED_INVENTORY_FIELDS = (
    "profile",
    "type",
    "content_role",
    "path_or_url",
    "scope",
    "inclusion_reason",
    "locator",
    "snapshot_locator",
    "read_method",
    "quality_check",
    "reliability",
    "status",
)
REQUIRED_PROCEDURE_BINDINGS = {
    "Procedure Trigger",
    "Procedure Decision Inputs",
    "Procedure Option Relationship",
    "Procedure Selection Rules",
    "Procedure Required Artifacts",
    "Procedure Verification",
}
REQUIRED_TASK_SECTIONS = (
    "## Project Background",
    "## Development Goal",
    "## Known Constraints",
    "## Expected Trigger",
    "## Acceptable Decision",
    "## Required Artifacts",
    "## Required Verification",
    "## Failure Conditions",
    "## Rubric",
    "## Review Record",
)
REQUIRED_RUBRIC_IDS = {
    "trigger-recognition",
    "decision-inputs",
    "option-relationship",
    "selection",
    "artifacts",
    "verification",
    "anti-pattern",
}
CRITICAL_RUBRIC_IDS = {
    "trigger-recognition",
    "option-relationship",
    "selection",
    "verification",
}
REQUIRED_DIFFICULTIES = {"typical", "boundary", "anti-pattern"}
VALID_MAPPING_STATUSES = {"mapped", "emerging", "excluded"}
VALID_CARD_REVIEW_DECISIONS = {"keep", "update", "split", "merge", "deprecate", "none"}
VALID_CARD_TYPES = {"atomic-decision", "composition-strategy"}


def validate_material_contract(manifest_path, inventory_path, claims):
    manifest = metadata(Path(manifest_path).read_text(encoding="utf-8"))
    if manifest.get("material_contract_version") != MATERIAL_CONTRACT_VERSION:
        return []

    errors = []
    for field in REQUIRED_MATERIAL_FIELDS:
        if not manifest.get(field):
            errors.append(f"v1 manifest missing {field}")

    profile = manifest.get("material_profile", "")
    if profile and profile not in VALID_MATERIAL_PROFILES:
        errors.append(f"v1 manifest has invalid material_profile: {profile}")

    material_state = manifest.get("material_state", "")
    if material_state and material_state not in VALID_MATERIAL_STATES:
        errors.append(f"v1 manifest has invalid material_state: {material_state}")
    if profile == "github-repository" and material_state in {"human-modified", "unknown"}:
        errors.append("github-repository material_state must be upstream-clean")

    boundary_rows = read_markdown_table_after_heading(manifest_path, "## Material Boundary")
    if not boundary_rows:
        errors.append("v1 manifest must contain Material Boundary rows")
    elif not any(row.get("include", "") for row in boundary_rows):
        errors.append("v1 Material Boundary must contain an included path")
    for row in boundary_rows:
        if row.get("exclude", "") and not row.get("exclusion_reason", ""):
            errors.append("v1 boundary exclusion requires exclusion_reason")

    inventory_rows = read_markdown_table(inventory_path)
    if not inventory_rows:
        errors.append("v1 inventory must contain a table")
    for row in inventory_rows:
        if row.get("include", "") != "yes":
            continue
        for field in REQUIRED_INCLUDED_INVENTORY_FIELDS:
            if not row.get(field, ""):
                errors.append(f"v1 included inventory unit missing {field}")

    for claim_id, claim in claims.items():
        if claim.get("content_role", "") not in VALID_CONTENT_ROLES:
            errors.append(f"v1 claim has invalid content_role: {claim_id}")
        if claim.get("source_position", "") not in VALID_SOURCE_POSITIONS:
            errors.append(f"v1 claim has invalid source_position: {claim_id}")
        if claim.get("conflict_status", "") not in VALID_CONFLICT_STATUSES:
            errors.append(f"v1 claim has invalid conflict_status: {claim_id}")
    return errors


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


def record_claim_ids(record):
    return claim_refs(record.get("claim_refs", ""))


def claim_reference_exists(reference, claims, source_packages):
    if "/" not in reference:
        return reference in claims
    source_id, claim_id = reference.split("/", 1)
    package = source_packages.get(source_id)
    return package is not None and claim_id in package["claims"]


def validate_decision_map_archives(derived, claims, source_packages):
    errors = []
    alignment = candidate_records(derived / "decision-map-alignment.md")
    proposals = candidate_records(derived / "map-change-proposals.md")
    reviews = candidate_records(derived / "card-review.md")

    if not alignment:
        errors.append("decision-map-alignment.md must contain a record")
    if not proposals:
        errors.append("map-change-proposals.md must contain a record")
    if not reviews:
        errors.append("card-review.md must contain a record")

    for record_id, record in alignment.items():
        mapping_status = record.get("mapping_status", "")
        if mapping_status not in VALID_MAPPING_STATUSES:
            errors.append(f"invalid mapping_status in decision-map-alignment.md: {record_id}")
        if mapping_status == "mapped" and not record.get("design_task_id"):
            errors.append(f"mapped alignment requires design_task_id: {record_id}")
        if mapping_status in {"emerging", "excluded"} and not record.get("mapping_reason"):
            errors.append(f"unmapped alignment requires mapping_reason: {record_id}")
        for claim_id in record_claim_ids(record):
            if not claim_reference_exists(claim_id, claims, source_packages):
                errors.append(f"decision-map-alignment.md references missing claim: {claim_id}")

    for record_id, record in proposals.items():
        proposal_type = record.get("proposal_type", "")
        if proposal_type not in {"none", "add", "split", "merge", "exclude"}:
            errors.append(f"invalid proposal_type in map-change-proposals.md: {record_id}")
        if not record.get("reason"):
            errors.append(f"map-change proposal requires reason: {record_id}")
        if proposal_type in {"add", "split"} and record.get("target_status") == "core":
            for field in (
                "proposed_task_id",
                "why_not_existing_task",
                "required_artifacts",
                "failure_risks",
                "child_problem_candidates",
                "coverage_maturity",
            ):
                if not record.get(field):
                    errors.append(f"core map proposal missing {field}: {record_id}")
        for claim_id in record_claim_ids(record):
            if not claim_reference_exists(claim_id, claims, source_packages):
                errors.append(f"map-change-proposals.md references missing claim: {claim_id}")

    for record_id, record in reviews.items():
        if record.get("decision") not in VALID_CARD_REVIEW_DECISIONS:
            errors.append(f"invalid card review decision: {record_id}")
        if not record.get("reason") or not record.get("next_action"):
            errors.append(f"card review requires reason and next_action: {record_id}")
        for claim_id in record_claim_ids(record):
            if not claim_reference_exists(claim_id, claims, source_packages):
                errors.append(f"card-review.md references missing claim: {claim_id}")
    return errors


def sidecar_bindings(path):
    text = path.read_text(encoding="utf-8")
    bindings = []
    for line in text.splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label, claim_text = line[2:].split(":", 1)
        bindings.append((label.strip(), claim_refs(claim_text)))
    return metadata(text), bindings


def cross_source_review_records(path):
    if not path.is_file():
        return {}
    return candidate_records(path)


def validate_cross_source_review(path):
    errors = []
    if not path.is_file():
        return ["v1 cross-source-review.md is required"]
    reviews = cross_source_review_records(path)
    if not reviews:
        return ["v1 cross-source-review.md must contain a record"]
    for review_id, review in reviews.items():
        status = review.get("status", "")
        if status not in VALID_CROSS_SOURCE_STATUSES:
            errors.append(f"invalid cross-source review status: {review_id}")
        if not review.get("candidate_id", ""):
            errors.append(f"cross-source review missing candidate_id: {review_id}")
        if not review.get("resolution_basis", ""):
            errors.append(f"cross-source review missing resolution_basis: {review_id}")
        if status == "distinct-scope" and not review.get("scope_conditions", ""):
            errors.append(f"distinct-scope review requires scope_conditions: {review_id}")
        if status == "superseded" and not review.get("superseding_claim_ref", ""):
            errors.append(f"superseded review requires superseding_claim_ref: {review_id}")
    return errors


def sibling_source_packages(package_root):
    packages = {}
    for sibling in Path(package_root).parent.glob("src-*"):
        manifest_path = sibling / "derived" / "manifest.md"
        ledger_path = sibling / "derived" / "evidence-ledger.md"
        if not manifest_path.is_file() or not ledger_path.is_file():
            continue
        manifest = metadata(manifest_path.read_text(encoding="utf-8"))
        source_id = manifest.get("source_id", "")
        if not source_id:
            continue
        claims = {
            row.get("claim_id"): row
            for row in read_markdown_table(ledger_path)
            if row.get("claim_id")
        }
        packages[source_id] = {"path": sibling, "claims": claims}
    return packages


def source_ids_from_value(value):
    return set(re.findall(r"\bsrc-\d{3}\b", value or ""))


def cross_source_errors(package_root, derived, draft_metadata, bindings):
    errors = []
    reviews = cross_source_review_records(derived / "cross-source-review.md")
    candidate_id = draft_metadata.get("candidate_id", "")
    source_ids = source_ids_from_value(draft_metadata.get("source_ids", ""))
    review_ids = set(REVIEW_REF_RE.findall(draft_metadata.get("cross_source_review_refs", "")))
    packages = sibling_source_packages(package_root)
    candidate_reviews = {
        review_id: review
        for review_id, review in reviews.items()
        if review.get("candidate_id", "") == candidate_id
    }

    for _, bound_refs in bindings:
        for reference in bound_refs:
            if "/" not in reference:
                continue
            source_id, claim_id = reference.split("/", 1)
            if source_id not in source_ids:
                errors.append(f"qualified claim source omitted from draft source_ids: {reference}")
                continue
            package = packages.get(source_id)
            if package is None:
                errors.append(f"qualified claim references unknown source: {reference}")
                continue
            if claim_id not in package["claims"]:
                errors.append(f"qualified claim references missing claim: {reference}")
                continue

            matching = [
                review
                for review_id, review in candidate_reviews.items()
                if review_id in review_ids
                if reference in claim_refs(review.get("claim_refs", ""))
            ]
            if not review_ids:
                errors.append(f"qualified claim requires cross_source_review_refs: {reference}")
                continue
            if not matching:
                errors.append(f"qualified claim has no cross-source review: {reference}")
                continue
            statuses = {review.get("status", "") for review in matching}
            if "unresolved" in statuses:
                errors.append(f"unresolved cross-source review: {reference}")
            if "distinct-scope" in statuses and not all(
                review.get("scope_conditions", "")
                for review in matching
                if review.get("status") == "distinct-scope"
            ):
                errors.append(f"distinct-scope review requires scope_conditions: {reference}")
            if "superseded" in statuses and not all(
                review.get("superseding_claim_ref", "")
                for review in matching
                if review.get("status") == "superseded"
            ):
                errors.append(f"superseded review requires superseding_claim_ref: {reference}")
    return errors


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


def markdown_section(text, heading):
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def bullet_values(text):
    values = {}
    for line in text.splitlines():
        match = re.match(r"^-\s+([a-z-]+):\s*(.+)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def validate_development_agent_evaluations(card_path, eval_root):
    errors = []
    card_path = Path(card_path)
    task_dir = Path(eval_root) / card_path.stem
    tasks = sorted(task_dir.glob("*.md")) if task_dir.is_dir() else []
    if len(tasks) != 3:
        return [f"{card_path.stem} requires exactly three evaluation tasks, found {len(tasks)}"]

    difficulties = []
    for task in tasks:
        text = task.read_text(encoding="utf-8")
        task_metadata = metadata(text)
        if task_metadata.get("card_id") != card_path.stem:
            errors.append(f"evaluation task card_id mismatch: {task.name}")
        difficulty = task_metadata.get("difficulty", "")
        difficulties.append(difficulty)
        if task_metadata.get("review_status") != "pass":
            errors.append(f"evaluation task must have review_status: pass: {task.name}")
        if not task_metadata.get("task_id"):
            errors.append(f"evaluation task missing task_id: {task.name}")
        if not task_metadata.get("reviewer"):
            errors.append(f"evaluation task missing reviewer: {task.name}")
        if not task_metadata.get("reviewed_at"):
            errors.append(f"evaluation task missing reviewed_at: {task.name}")
        for heading in REQUIRED_TASK_SECTIONS:
            if not markdown_section(text, heading):
                errors.append(f"evaluation task missing or empty section {heading}: {task.name}")
        if not markdown_section(text, "## Agent Response Summary"):
            errors.append(f"evaluation task missing or empty Agent Response Summary: {task.name}")

        rubric_ids = set(bullet_values(markdown_section(text, "## Rubric")))
        missing_rubric_ids = REQUIRED_RUBRIC_IDS - rubric_ids
        if missing_rubric_ids:
            errors.append(
                f"evaluation task missing rubric IDs {', '.join(sorted(missing_rubric_ids))}: {task.name}"
            )
        review = bullet_values(markdown_section(text, "## Review Record"))
        missing_review_ids = REQUIRED_RUBRIC_IDS - set(review)
        if missing_review_ids:
            errors.append(
                f"evaluation task missing review outcomes {', '.join(sorted(missing_review_ids))}: {task.name}"
            )
            continue
        for rubric_id in REQUIRED_RUBRIC_IDS:
            outcome = review[rubric_id]
            if outcome not in {"pass", "partial", "fail"}:
                errors.append(f"invalid review outcome for {rubric_id}: {task.name}")
        for rubric_id in CRITICAL_RUBRIC_IDS:
            if review.get(rubric_id) == "fail":
                errors.append(f"critical rubric failure {rubric_id}: {task.name}")
        partial_count = sum(
            review.get(rubric_id) == "partial"
            for rubric_id in REQUIRED_RUBRIC_IDS - CRITICAL_RUBRIC_IDS
        )
        if partial_count > 1:
            errors.append(f"evaluation task has more than one non-critical partial: {task.name}")

    if set(difficulties) != REQUIRED_DIFFICULTIES or len(set(difficulties)) != 3:
        errors.append(
            f"evaluation tasks must use unique difficulties: {', '.join(sorted(REQUIRED_DIFFICULTIES))}"
        )
    return errors


def load_core_tasks(cards_dir):
    map_path = Path(cards_dir).parent / "DECISION-MAP.md"
    if not map_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "validate_card_for_distillation", Path(__file__).with_name("validate_card.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_decision_map(map_path)


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

    manifest_path = derived / "manifest.md"
    inventory_path = derived / "inventory.md"
    manifest_data = metadata(manifest_path.read_text(encoding="utf-8"))
    material_contract_v1 = manifest_data.get("material_contract_version") == MATERIAL_CONTRACT_VERSION
    source_id = manifest_data.get("source_id", "")
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

    errors.extend(validate_material_contract(manifest_path, inventory_path, claims))
    if material_contract_v1:
        errors.extend(validate_cross_source_review(derived / "cross-source-review.md"))

    try:
        core_tasks = load_core_tasks(cards_dir)
    except (OSError, ValueError) as error:
        errors.append(f"invalid decision map for distillation: {error}")
        core_tasks = None

    for candidate_id, candidate in candidates.items():
        if material_contract_v1:
            candidate_source_ids = source_ids_from_value(candidate.get("source_ids", ""))
            candidate_review_ids = set(REVIEW_REF_RE.findall(candidate.get("cross_source_review_refs", "")))
            if not candidate_source_ids:
                errors.append(f"v1 candidate missing source_ids: {candidate_id}")
            if len(candidate_source_ids) > 1 and not candidate_review_ids:
                errors.append(f"multi-source candidate missing cross_source_review_refs: {candidate_id}")
        task_id = candidate.get("design_task_id", "")
        if task_id:
            if candidate.get("status") in {"new", "merge-with-existing"}:
                if candidate.get("card_type") not in VALID_CARD_TYPES:
                    errors.append(f"publishable candidate missing valid card_type: {candidate_id}")
                if not candidate.get("benchmark_task_ids"):
                    errors.append(f"publishable candidate missing benchmark_task_ids: {candidate_id}")
            if core_tasks is not None and (
                task_id not in core_tasks or core_tasks[task_id].get("status") != "core"
            ):
                errors.append(f"candidate must bind a known core design_task_id: {candidate_id}")
            continue
        if candidate.get("mapping_status") in {"emerging", "excluded"} and candidate.get("mapping_reason"):
            if candidate.get("target_contract") == DEVELOPMENT_AGENT_CONTRACT:
                errors.append(f"development-agent-v1 candidate requires design_task_id: {candidate_id}")
            continue
        errors.append(f"candidate requires design_task_id or mapping_status/reason: {candidate_id}")

    errors.extend(validate_decision_map_archives(derived, claims, sibling_source_packages(package_root)))

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
        if material_contract_v1:
            draft_source_ids = source_ids_from_value(draft_metadata.get("source_ids", ""))
            draft_review_ids = set(REVIEW_REF_RE.findall(draft_metadata.get("cross_source_review_refs", "")))
            if not draft_source_ids:
                errors.append(f"v1 draft missing source_ids: {draft.name}")
            if len(draft_source_ids) > 1 and not draft_review_ids:
                errors.append(f"multi-source draft missing cross_source_review_refs: {draft.name}")
        if not bindings or not any(claim_ids for _, claim_ids in bindings):
            errors.append(f"evidence sidecar has no claim IDs: {sidecar.name}")
            continue
        for label, claim_ids in bindings:
            for claim_id in claim_ids:
                if "/" in claim_id:
                    continue
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
                if material_contract_v1 and draft_metadata.get("status") == "published":
                    if claim.get("source_position", "") == "auxiliary":
                        errors.append(f"published binding uses auxiliary source_position: {claim_id}")
                    if claim.get("conflict_status", "") == "unresolved":
                        errors.append(f"published binding uses unresolved conflict_status: {claim_id}")

        if material_contract_v1 and draft_metadata.get("status") == "published":
            errors.extend(cross_source_errors(package_root, derived, draft_metadata, bindings))

        if draft_metadata.get("status") == "published":
            card = published_card_path(draft_metadata.get("published_card", ""), cards_dir)
            if card and card.is_file():
                card_metadata = metadata(card.read_text(encoding="utf-8"))
                if card_metadata.get("card_contract") == DEVELOPMENT_AGENT_CONTRACT:
                    for field in (
                        "design_task_id",
                        "design_goal",
                        "required_artifact_types",
                        "failure_risks",
                        "card_type",
                        "utility_status",
                    ):
                        if not draft_metadata.get(field):
                            errors.append(f"v1 draft missing {field}: {draft.name}")
                        elif draft_metadata.get(field) != card_metadata.get(field):
                            errors.append(f"v1 draft {field} does not match published card: {draft.name}")
                    binding_labels = {label for label, _ in bindings}
                    missing_bindings = REQUIRED_PROCEDURE_BINDINGS - binding_labels
                    if missing_bindings:
                        errors.append(
                            f"v1 draft missing Procedure bindings {', '.join(sorted(missing_bindings))}: {draft.name}"
                        )
                    eval_root = cards_dir.parent / "eval" / "development-agent"
                    errors.extend(validate_development_agent_evaluations(card, eval_root))

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
