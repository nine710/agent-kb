import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_card.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_card", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_card(path: Path, contract="decision-card-v0", procedure=True, relationship="exclusive", consumer="development-agent"):
    procedure_body = ""
    if procedure:
        procedure_body = """
## Development Agent Procedure

### Trigger
Use this when the task needs an Agent design decision.

### Decision Inputs
Collect project constraints.

### Option Relationship
Options are exclusive.

### Selection Rules
Select the option matching the constraints.

### Required Artifacts
Produce an architecture record and tests.

### Verification
Run the design checks.
"""
    consumer_fields = (
        f"consumer: {consumer}\n"
        "decision_scope: agent-runtime-architecture\n"
        f"option_relationship: {relationship}\n"
        if contract == "development-agent-v1"
        else ""
    )
    path.write_text(
        "---\n"
        "id: example-card\n"
        f"card_contract: {contract}\n"
        f"{consumer_fields}"
        "problem: Which architecture should the Agent use?\n"
        "tags: [harness]\n"
        "when_to_use: When architecture is under design.\n"
        "when_not: When no design decision exists.\n"
        "status: active\n"
        "source_ids: [src-001]\n"
        "---\n\n"
        "## Options\n\n"
        "### Option A: First\nA path.\n\n"
        "### Option B: Second\nB path.\n\n"
        "### Option C: Third\nC path.\n\n"
        "## Tradeoffs\n\n| | Advantage | Cost |\n|---|---|---|\n| A | x | y |\n| B | x | y |\n| C | x | y |\n\n"
        "## Apply to Agent Development\n\nUse the selected path.\n\n"
        + procedure_body
        + "\n## Anti-Patterns\n\nDo not ignore constraints.\n\n"
        "## Sources\n\n- [src-001] chapter1.md §Agent\n",
        encoding="utf-8",
    )
    return path


class ValidateCardContractTests(unittest.TestCase):
    def test_accepts_decision_card_v0_without_procedure(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", procedure=False)
            errors, _ = validator.validate(str(path))
            self.assertEqual([], errors)

    def test_accepts_complete_development_agent_v1_card(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", contract="development-agent-v1")
            errors, _ = validator.validate(str(path))
            self.assertEqual([], errors)

    def test_rejects_v1_card_missing_procedure_heading(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", contract="development-agent-v1", procedure=False)
            errors, _ = validator.validate(str(path))
            self.assertTrue(any("Development Agent Procedure" in error for error in errors))

    def test_rejects_v1_card_with_unknown_option_relationship(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", contract="development-agent-v1", relationship="mixed")
            errors, _ = validator.validate(str(path))
            self.assertTrue(any("option_relationship" in error for error in errors))

    def test_rejects_v1_card_missing_consumer(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", contract="development-agent-v1", consumer="")
            errors, _ = validator.validate(str(path))
            self.assertTrue(any("consumer" in error for error in errors))

    def test_rejects_v1_card_with_empty_verification(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md", contract="development-agent-v1")
            text = path.read_text(encoding="utf-8").replace("### Verification\nRun the design checks.", "### Verification\n\n## Anti-Patterns")
            path.write_text(text, encoding="utf-8")
            errors, _ = validator.validate(str(path))
            self.assertTrue(any("Verification" in error for error in errors))

    def test_rejects_card_missing_contract(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_card(Path(temp_dir) / "example-card.md")
            path.write_text(path.read_text(encoding="utf-8").replace("card_contract: decision-card-v0\n", ""), encoding="utf-8")
            errors, _ = validator.validate(str(path))
            self.assertTrue(any("card_contract" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
