import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_distillation.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_distillation", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_package(
    root: Path,
    support_status="supported",
    reliability="high",
    candidate_status="new",
    inference_chain="",
):
    derived = root / "derived"
    derived.mkdir(parents=True)
    (derived / "manifest.md").write_text("# Manifest\n\n- source_id: src-001\n", encoding="utf-8")
    (derived / "inventory.md").write_text("# Inventory\n\n- chapter1.md | high\n", encoding="utf-8")
    (derived / "progress.md").write_text("# Progress\n\nstage: completed\nlast_locator: chapter1.md\n", encoding="utf-8")
    (derived / "evidence-ledger.md").write_text(
        "# Evidence Ledger\n\n"
        "| claim_id | claim | locator | support_status | reliability | candidate_refs | card_refs | inference_chain |\n"
        "|---|---|---|---|---|---|---|---|\n"
        f"| CLM-001 | supported claim | chapter1.md#choice | {support_status} | {reliability} | candidate-three-way | option-a | {inference_chain} |\n",
        encoding="utf-8",
    )
    (derived / "candidate-problems.md").write_text(
        "# Candidate Problems\n\n"
        "## candidate-three-way\n\n"
        f"status: {candidate_status}\n\n"
        "claim_refs: CLM-001\n\n"
        "three_way_assessment: pass\n",
        encoding="utf-8",
    )
    (derived / "distillation-report.md").write_text("# Distillation Report\n\nstatus: completed\n", encoding="utf-8")


def write_draft(drafts: Path, source_id="src-001", candidate_id="candidate-three-way"):
    (drafts / "example.md").write_text(
        f"---\nid: example\nsource_ids: [{source_id}]\n---\n", encoding="utf-8"
    )
    (drafts / "example.evidence.md").write_text(
        "# Evidence Binding\n\n"
        f"source_id: {source_id}\n"
        f"candidate_id: {candidate_id}\n\n"
        "- Option A: CLM-001\n",
        encoding="utf-8",
    )


class ValidateDistillationTests(unittest.TestCase):
    def test_accepts_complete_publishable_package(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_rejects_draft_bound_to_unsupported_claim(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, support_status="unsupported")
            write_draft(drafts)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("CLM-001" in error and "unsupported" in error for error in errors))

    def test_rejects_missing_evidence_sidecar(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            (drafts / "example.md").write_text(
                "---\nid: example\nsource_ids: [src-001]\n---\n", encoding="utf-8"
            )
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("example.evidence.md" in error for error in errors))

    def test_rejects_draft_bound_to_low_reliability_claim(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, reliability="low")
            write_draft(drafts)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("CLM-001" in error and "low-reliability" in error for error in errors))

    def test_ignores_draft_owned_by_a_different_source(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts, source_id="src-002", candidate_id="candidate-other")
            (drafts / "example.evidence.md").write_text(
                "# Evidence Binding\n\n"
                "source_id: src-002\n"
                "candidate_id: candidate-other\n\n"
                "- Option A: CLM-999\n",
                encoding="utf-8",
            )
            self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_rejects_draft_bound_to_raw_only_candidate(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, candidate_status="raw-only")
            write_draft(drafts)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("candidate-three-way" in error and "raw-only" in error for error in errors))

    def test_rejects_inferred_claim_bound_to_an_option(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, support_status="inferred", inference_chain="CLM-002")
            write_draft(drafts)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("Option A" in error and "supported" in error for error in errors))

    def test_rejects_published_card_with_non_active_status(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            (cards / "example.md").write_text("---\nid: example\nstatus: draft\n---\n", encoding="utf-8")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("example.md" in error and "active" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
