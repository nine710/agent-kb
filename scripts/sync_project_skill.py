"""Synchronize the reviewed project skill into Codex's repository skill path."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "agent-kb-distill"
TARGET = ROOT / ".agents" / "skills" / "agent-kb-distill"


def relative_files(path: Path) -> set[Path]:
    return {
        item.relative_to(path)
        for item in path.rglob("*")
        if item.is_file()
    }


def differences() -> list[str]:
    if not SOURCE.is_dir():
        return [f"missing source: {SOURCE}"]
    if not TARGET.is_dir():
        return [f"missing target: {TARGET}"]

    source_files = relative_files(SOURCE)
    target_files = relative_files(TARGET)
    changes = [f"missing target file: {item}" for item in sorted(source_files - target_files)]
    changes.extend(f"stale target file: {item}" for item in sorted(target_files - source_files))

    for item in sorted(source_files & target_files):
        if not filecmp.cmp(SOURCE / item, TARGET / item, shallow=False):
            changes.append(f"different: {item}")
    return changes


def sync() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Source skill does not exist: {SOURCE}")

    TARGET.mkdir(parents=True, exist_ok=True)
    for item in sorted(relative_files(TARGET) - relative_files(SOURCE)):
        (TARGET / item).unlink()
    for item in sorted(relative_files(SOURCE)):
        destination = TARGET / item
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / item, destination)

    for directory in sorted(
        (path for path in TARGET.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if not any(directory.iterdir()):
            directory.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or sync the canonical project skill to .agents/skills."
    )
    parser.add_argument(
        "action",
        choices=("check", "sync"),
        nargs="?",
        default="check",
        help="check for drift (default) or copy the reviewed source to Codex's target",
    )
    args = parser.parse_args()

    if args.action == "sync":
        sync()

    changes = differences()
    if changes:
        for change in changes:
            print(change)
        return 1

    print("project skill source and Codex mirror are synchronized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
