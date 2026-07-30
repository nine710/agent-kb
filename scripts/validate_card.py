#!/usr/bin/env python3
"""validate_card.py — Validate a decision card against SCHEMA.md rules.

Usage:
    python scripts/validate_card.py cards/constraint-placement.md
    python scripts/validate_card.py --all
"""
import os
import re
import sys


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


def validate(path):
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
