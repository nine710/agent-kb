#!/usr/bin/env python3
"""Validate the independent development-agent benchmark task set."""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "## Project Background",
    "## Development Goal",
    "## Known Constraints",
    "## Required Artifacts",
    "## Failure Risks",
    "## Independent Rubric",
)
RESPONSIBILITIES = {
    "goal-and-task-execution-architecture",
    "context-and-state-architecture",
    "knowledge-and-memory-architecture",
    "tool-and-action-architecture",
    "safety-and-human-control-architecture",
    "evaluation-and-observability-architecture",
    "continuous-improvement-and-collaboration-architecture",
}
FORBIDDEN_PROMPT_MARKERS = (
    "Acceptable Decision",
    "Option A",
    "Option B",
    "Option C",
    "card_id:",
    "card_contract:",
)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    result = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip("'\"")
    return result


def section_has_content(text, heading):
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return bool(match and match.group(1).strip())


def validate(root):
    root = Path(root)
    errors = []
    tasks = sorted(root.glob("task-*.md")) if root.is_dir() else []
    if len(tasks) != 7:
        errors.append(f"benchmark requires exactly seven task files, found {len(tasks)}")

    seen_ids = set()
    seen_responsibilities = set()
    for task in tasks:
        text = task.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        for field in ("task_id", "responsibility_id", "difficulty", "review_status"):
            if not metadata.get(field):
                errors.append(f"{task.name} missing frontmatter field: {field}")
        task_id = metadata.get("task_id", "")
        if task_id in seen_ids:
            errors.append(f"duplicate task_id: {task_id}")
        seen_ids.add(task_id)
        responsibility = metadata.get("responsibility_id", "")
        if responsibility not in RESPONSIBILITIES:
            errors.append(f"{task.name} has invalid responsibility_id: {responsibility}")
        seen_responsibilities.add(responsibility)
        if metadata.get("difficulty") != "typical":
            errors.append(f"{task.name} must use difficulty: typical for the pilot")
        if metadata.get("review_status") not in {"pending", "pass", "fail"}:
            errors.append(f"{task.name} has invalid review_status")
        for heading in REQUIRED_SECTIONS:
            if not section_has_content(text, heading):
                errors.append(f"{task.name} missing or empty section: {heading}")
        for marker in FORBIDDEN_PROMPT_MARKERS:
            if marker in text:
                errors.append(f"{task.name} exposes forbidden answer/card marker: {marker}")
        if "## Options" in text:
            errors.append(f"{task.name} must not contain an Options section")

    missing = sorted(RESPONSIBILITIES - seen_responsibilities)
    if missing:
        errors.append(f"benchmark is missing responsibilities: {', '.join(missing)}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark_root", type=Path)
    args = parser.parse_args()
    errors = validate(args.benchmark_root)
    if errors:
        print(f"FAIL: {args.benchmark_root}")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1
    print(f"PASS: {args.benchmark_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
