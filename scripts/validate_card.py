#!/usr/bin/env python3
"""validate_card.py — Validate a decision card against SCHEMA.md rules.

Usage:
    python scripts/validate_card.py cards/constraint-placement.md
    python scripts/validate_card.py --all
"""
import os
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = [
    "id", "problem", "tags", "when_to_use", "when_not", "status", "source_ids",
]
REQUIRED_SECTIONS = [
    "## Options",
    "## Tradeoffs",
    "## Apply to Agent Development",
    "## Anti-Patterns",
    "## Sources",
]
VALID_CARD_CONTRACTS = {"decision-card-v0", "development-agent-v1"}
VALID_DECISION_SCOPES = {
    "agent-runtime-architecture",
    "knowledge-retrieval",
    "evaluation",
    "continuous-improvement",
    "multi-agent-topology",
}
VALID_OPTION_RELATIONSHIPS = {
    "exclusive",
    "composable",
    "layered",
    "sequential",
    "composable-by-information-type",
}
PROCEDURE_SUBSECTIONS = [
    "### Trigger",
    "### Decision Inputs",
    "### Option Relationship",
    "### Selection Rules",
    "### Required Artifacts",
    "### Verification",
]
DECISION_MAP_FIELDS = {
    "id",
    "name",
    "status",
    "design_goal",
    "required_artifacts",
    "failure_risks",
    "child_problems",
    "coverage_status",
    "coverage_cards",
    "coverage_raw_only",
    "coverage_evidence_needed",
}
DECISION_MAP_LIST_FIELDS = {
    "required_artifacts",
    "failure_risks",
    "child_problems",
    "coverage_cards",
    "coverage_raw_only",
    "coverage_evidence_needed",
}
DECISION_TASK_STATUSES = {"core", "emerging", "excluded"}
COVERAGE_STATUSES = {"covered", "partial", "no-published-card"}
REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(text):
    """Extract YAML frontmatter as dict (minimal parser, no PyYAML)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                items = [
                    v.strip().strip("'\"")
                    for v in val[1:-1].split(",")
                    if v.strip()
                ]
                result[key] = items
            else:
                result[key] = val
    return result


def extract_body(text):
    """Return text after frontmatter."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:]


def count_options(body):
    """Count '### Option' headings."""
    return len(re.findall(r"^### Option", body, re.MULTILINE))


def section_has_content(body, heading):
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^### |^## |\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return bool(match and match.group(1).strip())


def parse_map_list(value):
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError(f"map list must use [item, item] syntax: {value}")
    return [item.strip() for item in value[1:-1].split(",") if item.strip()]


def load_decision_map(path):
    """Return a decision-task mapping keyed by id from a flat Markdown registry."""
    text = Path(path).read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## ([a-z0-9-]+)\s*$", text, re.MULTILINE))
    if not matches:
        raise ValueError("decision map has no task sections")

    tasks = {}
    for index, match in enumerate(matches):
        heading_id = match.group(1)
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        record = {}
        for line in text[match.end():block_end].splitlines():
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                raise ValueError(f"invalid map line in {heading_id}: {line}")
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if key not in DECISION_MAP_FIELDS:
                raise ValueError(f"unknown map field in {heading_id}: {key}")
            if key in record:
                raise ValueError(f"duplicate map field in {heading_id}: {key}")
            record[key] = parse_map_list(value) if key in DECISION_MAP_LIST_FIELDS else value
        record["_heading_id"] = heading_id
        task_id = record.get("id", heading_id)
        if task_id in tasks:
            raise ValueError(f"duplicate decision map id: {task_id}")
        tasks[task_id] = record

    errors = validate_decision_map(tasks)
    if errors:
        raise ValueError("; ".join(errors))
    return tasks


def validate_decision_map(tasks):
    """Return structural errors without inspecting card files."""
    errors = []
    for task_id, task in tasks.items():
        for field in DECISION_MAP_FIELDS:
            if field not in task:
                errors.append(f"decision map {task_id} missing field: {field}")
        if task.get("id") != task.get("_heading_id"):
            errors.append(f"decision map id does not match heading: {task_id}")
        if task.get("status") not in DECISION_TASK_STATUSES:
            errors.append(f"decision map {task_id} has invalid status")
        if task.get("coverage_status") not in COVERAGE_STATUSES:
            errors.append(f"decision map {task_id} has invalid coverage_status")
        for field in ("required_artifacts", "failure_risks", "child_problems"):
            if not task.get(field):
                errors.append(f"decision map {task_id} requires non-empty {field}")
        coverage_status = task.get("coverage_status")
        coverage_cards = task.get("coverage_cards", [])
        raw_only = task.get("coverage_raw_only", [])
        evidence_needed = task.get("coverage_evidence_needed", [])
        if coverage_status == "covered" and not coverage_cards:
            errors.append(f"decision map {task_id} covered status requires coverage_cards")
        if coverage_status == "partial" and (not coverage_cards or not raw_only):
            errors.append(f"decision map {task_id} partial status requires cards and raw-only gaps")
        if coverage_status == "no-published-card" and (coverage_cards or not evidence_needed):
            errors.append(f"decision map {task_id} no-published-card status requires evidence gap")
    return errors


def decision_map_path_for_card(card_path, explicit_path):
    if explicit_path:
        return Path(explicit_path)
    if Path(card_path).resolve().parent == REPO_ROOT / "cards":
        return REPO_ROOT / "DECISION-MAP.md"
    return None


def validate_decision_map_binding(fm, map_path):
    errors = []
    if map_path is None:
        return errors
    try:
        tasks = load_decision_map(map_path)
    except (OSError, ValueError) as error:
        return [f"invalid decision map: {error}"]

    task_id = fm.get("design_task_id", "")
    if not task_id:
        return ["development-agent-v1 cards require design_task_id"]
    task = tasks.get(task_id)
    if not task:
        return [f"unknown design_task_id: {task_id}"]
    if task["status"] != "core":
        return [f"design_task_id must reference a core task: {task_id}"]
    if fm.get("design_goal") != task["design_goal"]:
        errors.append("design_goal must exactly match the decision map task")
    for field, allowed in (
        ("required_artifact_types", task["required_artifacts"]),
        ("failure_risks", task["failure_risks"]),
    ):
        values = fm.get(field, [])
        if not isinstance(values, list) or not values:
            errors.append(f"development-agent-v1 cards require non-empty {field}")
            continue
        unknown_values = sorted(set(values) - set(allowed))
        if unknown_values:
            errors.append(f"{field} not allowed by design task: {', '.join(unknown_values)}")
    return errors


def validate(path, decision_map_path=None):
    """Return (errors, warnings) for a card file."""
    errors = []
    warnings = []

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    fm = parse_frontmatter(text)
    body = extract_body(text)

    # 1. Required frontmatter fields
    for field in REQUIRED_FRONTMATTER:
        if field not in fm or not fm[field]:
            errors.append(f"missing or empty frontmatter field: {field}")

    # 2. status must be 'active' in cards/
    if fm.get("status") and fm["status"] != "active":
        errors.append(f"status must be 'active' in cards/, got: '{fm.get('status')}'")

    # 2b. Staged consumer-facing card contract
    contract = fm.get("card_contract", "")
    if not contract:
        errors.append("missing or empty frontmatter field: card_contract")
    elif contract not in VALID_CARD_CONTRACTS:
        errors.append(f"invalid card_contract: {contract}")
    elif contract == "development-agent-v1":
        if fm.get("consumer") != "development-agent":
            errors.append("development-agent-v1 cards require consumer: development-agent")
        if fm.get("decision_scope") not in VALID_DECISION_SCOPES:
            errors.append(f"invalid or missing decision_scope: {fm.get('decision_scope', '')}")
        if fm.get("option_relationship") not in VALID_OPTION_RELATIONSHIPS:
            errors.append(f"invalid or missing option_relationship: {fm.get('option_relationship', '')}")
        if "## Development Agent Procedure" not in body:
            errors.append("missing section: ## Development Agent Procedure")
        else:
            for heading in PROCEDURE_SUBSECTIONS:
                if not section_has_content(body, heading):
                    errors.append(f"missing or empty Procedure subsection: {heading}")
        errors.extend(validate_decision_map_binding(fm, decision_map_path_for_card(path, decision_map_path)))

    # 3. Options >= 3
    opt_count = count_options(body)
    if opt_count < 3:
        errors.append(f"Options must be >= 3, found {opt_count}")

    # 4. Required sections
    for sec in REQUIRED_SECTIONS:
        if sec not in body:
            errors.append(f"missing section: {sec}")

    # 5. Sources must contain src- references
    sources_idx = body.find("## Sources")
    if sources_idx != -1:
        sources_text = body[sources_idx:]
        if "src-" not in sources_text:
            warnings.append("Sources section has no src- ID references")

    # 6. id should match filename
    filename = os.path.splitext(os.path.basename(path))[0]
    if fm.get("id") and fm["id"] != filename:
        errors.append(f"id '{fm['id']}' does not match filename '{filename}'")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_card.py <card.md>")
        print("       python scripts/validate_card.py --all")
        sys.exit(2)

    if sys.argv[1] == "--all":
        card_dir = os.path.join(os.path.dirname(__file__), "..", "cards")
        if not os.path.isdir(card_dir):
            print("No cards/ directory found")
            sys.exit(0)
        cards = sorted(
            os.path.join(card_dir, f)
            for f in os.listdir(card_dir)
            if f.endswith(".md")
        )
        if not cards:
            print("No cards to validate")
            sys.exit(0)
    else:
        cards = [sys.argv[1]]

    has_errors = False
    for card in cards:
        errors, warnings = validate(card)
        rel = os.path.relpath(card)
        if errors:
            has_errors = True
            print(f"FAIL: {rel}")
            for e in errors:
                print(f"  ERROR: {e}")
        elif warnings:
            print(f"WARN: {rel}")
            for w in warnings:
                print(f"  WARN: {w}")
        else:
            print(f"PASS: {rel}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
