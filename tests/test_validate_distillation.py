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
    candidate_id="candidate-three-way",
    three_way_assessment="pass",
    include_map_archives=True,
    design_task_id="context-and-state-architecture",
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
        f"## {candidate_id}\n\n"
        f"status: {candidate_status}\n\n"
        f"design_task_id: {design_task_id}\n\n"
        "claim_refs: CLM-001\n\n"
        f"three_way_assessment: {three_way_assessment}\n",
        encoding="utf-8",
    )
    (derived / "distillation-report.md").write_text("# Distillation Report\n\nstatus: completed\n", encoding="utf-8")
    if include_map_archives:
        write_map_archives(derived)


def write_map_archives(derived: Path):
    (derived / "decision-map-alignment.md").write_text(
        "# Decision Map Alignment\n\n## alignment-001\n\n"
        "claim_refs: CLM-001\n"
        "mapping_status: mapped\n"
        "design_task_id: context-and-state-architecture\n"
        "affected_cards: example\n",
        encoding="utf-8",
    )
    (derived / "map-change-proposals.md").write_text(
        "# Map Change Proposals\n\n## proposal-001\n\n"
        "proposal_type: none\n"
        "claim_refs: CLM-001\n"
        "reason: No map change from this source.\n",
        encoding="utf-8",
    )
    (derived / "card-review.md").write_text(
        "# Card Review\n\n## review-001\n\n"
        "decision: keep\n"
        "claim_refs: CLM-001\n"
        "reason: Existing card remains applicable.\n"
        "next_action: keep\n",
        encoding="utf-8",
    )


def write_draft(
    drafts: Path,
    source_id="src-001",
    candidate_id="candidate-three-way",
    status="published",
    published_card="example",
    decision_reason="",
    filename="example",
):
    source_drafts = drafts / source_id
    source_drafts.mkdir(parents=True, exist_ok=True)
    published_line = f"published_card: {published_card}\n" if published_card else ""
    reason_line = f"decision_reason: {decision_reason}\n" if decision_reason else ""
    (source_drafts / f"{filename}.md").write_text(
        "---\n"
        f"id: {filename}\n"
        f"source_id: {source_id}\n"
        f"source_ids: [{source_id}]\n"
        f"candidate_id: {candidate_id}\n"
        "design_task_id: context-and-state-architecture\n"
        "design_goal: 让 Agent 在任务全过程获得正确、足够、可恢复的信息。\n"
        "required_artifact_types: [context-layering-table]\n"
        "failure_risks: [context-corruption]\n"
        f"status: {status}\n"
        f"{published_line}"
        f"{reason_line}"
        "---\n",
        encoding="utf-8",
    )
    (source_drafts / f"{filename}.evidence.md").write_text(
        "# Evidence Binding\n\n"
        f"source_id: {source_id}\n"
        f"candidate_id: {candidate_id}\n\n"
        "- Option A: CLM-001\n",
        encoding="utf-8",
    )


def write_v1_card(cards: Path):
    (cards / "example.md").write_text(
        "---\n"
        "id: example\n"
        "card_contract: development-agent-v1\n"
        "consumer: development-agent\n"
        "decision_scope: agent-runtime-architecture\n"
        "option_relationship: exclusive\n"
        "design_task_id: context-and-state-architecture\n"
        "design_goal: 让 Agent 在任务全过程获得正确、足够、可恢复的信息。\n"
        "required_artifact_types: [context-layering-table]\n"
        "failure_risks: [context-corruption]\n"
        "status: active\n"
        "---\n\n"
        "## Development Agent Procedure\n\n"
        "### Trigger\nTrigger.\n\n"
        "### Decision Inputs\nInputs.\n\n"
        "### Option Relationship\nExclusive.\n\n"
        "### Selection Rules\nRules.\n\n"
        "### Required Artifacts\nArtifacts.\n\n"
        "### Verification\nVerification.\n",
        encoding="utf-8",
    )
def write_evaluation_task(
    cards: Path,
    difficulty: str,
    critical_result="pass",
    include_anti_pattern=True,
    reviewer="test reviewer",
    reviewed_at="2026-08-01",
    response_summary="The Agent made a reviewed decision.",
):
    task_dir = cards.parent / "eval" / "development-agent" / "example"
    task_dir.mkdir(parents=True, exist_ok=True)
    rubric = [
        "trigger-recognition",
        "decision-inputs",
        "option-relationship",
        "selection",
        "artifacts",
        "verification",
    ]
    if include_anti_pattern:
        rubric.append("anti-pattern")
    rubric_body = "\n".join(f"- {item}: criterion" for item in rubric)
    review_body = "\n".join(
        f"- {item}: {critical_result if item == 'selection' else 'pass'}" for item in rubric
    )
    (task_dir / f"{difficulty}.md").write_text(
        "---\n"
        "card_id: example\n"
        f"task_id: example-{difficulty}\n"
        f"difficulty: {difficulty}\n"
        "review_status: pass\n"
        f"reviewer: {reviewer}\n"
        f"reviewed_at: {reviewed_at}\n"
        "---\n\n"
        "## Project Background\nBackground.\n\n"
        "## Development Goal\nGoal.\n\n"
        "## Known Constraints\nConstraints.\n\n"
        "## Expected Trigger\nTrigger.\n\n"
        "## Acceptable Decision\nDecision.\n\n"
        "## Required Artifacts\nArtifacts.\n\n"
        "## Required Verification\nVerification.\n\n"
        "## Failure Conditions\nFailure.\n\n"
        "## Rubric\n"
        f"{rubric_body}\n\n"
        "## Review Record\n"
        f"{review_body}\n\n"
        "## Agent Response Summary\n"
        f"{response_summary}\n",
        encoding="utf-8",
    )


def add_procedure_bindings(drafts: Path):
    sidecar = drafts / "src-001" / "example.evidence.md"
    with sidecar.open("a", encoding="utf-8") as handle:
        for label in (
            "Procedure Trigger",
            "Procedure Decision Inputs",
            "Procedure Option Relationship",
            "Procedure Selection Rules",
            "Procedure Required Artifacts",
            "Procedure Verification",
        ):
            handle.write(f"- {label}: CLM-001\n")


class ValidateDistillationTests(unittest.TestCase):
    def test_rejects_package_without_decision_map_archives(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, include_map_archives=False)
            write_draft(drafts)
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("decision-map-alignment.md" in error for error in errors))

    def test_rejects_candidate_without_design_task_or_mapping_reason(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, design_task_id="")
            write_draft(drafts)
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("design_task_id" in error for error in errors))

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
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
            self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_accepts_all_lifecycle_states(self):
        validator = load_validator()
        for status in ("draft", "published", "raw-only", "out-of-scope", "rejected"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir) / "src-001-example"
                drafts = Path(temp_dir) / "drafts"
                cards = Path(temp_dir) / "cards"
                drafts.mkdir()
                cards.mkdir()
                candidate_id = f"candidate-{status}"
                candidate_status = "new" if status in {"draft", "published"} else status
                assessment = "pass" if status in {"draft", "published"} else "fail"
                write_package(
                    root,
                    candidate_id=candidate_id,
                    candidate_status=candidate_status,
                    three_way_assessment=assessment,
                )
                write_draft(
                    drafts,
                    candidate_id=candidate_id,
                    status=status,
                    published_card="example" if status == "published" else "",
                    decision_reason="withheld by scope" if status not in {"draft", "published"} else "",
                    filename=status,
                )
                if status == "published":
                    (cards / "example.md").write_text(
                        "---\nid: example\nstatus: active\n---\n", encoding="utf-8"
                    )
                self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_rejects_published_draft_without_published_card(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts, published_card="")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("published_card" in error for error in errors))

    def test_rejects_non_published_draft_with_published_card(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts, status="raw-only", published_card="example", decision_reason="only two paths")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("must not set published_card" in error for error in errors))

    def test_rejects_unknown_draft_status(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts, status="archived", published_card="", decision_reason="legacy")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("unknown draft status" in error for error in errors))

    def test_rejects_orphan_candidate_and_duplicate_archive(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            write_draft(drafts, filename="duplicate")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("duplicate candidate_id" in error for error in errors))

    def test_rejects_candidate_without_archive(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("missing draft archive" in error for error in errors))

    def test_rejects_sidecar_with_mismatched_candidate_id(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
            sidecar = drafts / "src-001" / "example.evidence.md"
            sidecar.write_text(
                "# Evidence Binding\n\n"
                "source_id: src-001\n"
                "candidate_id: candidate-other\n\n"
                "- Option A: CLM-001\n",
                encoding="utf-8",
            )
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("candidate_id does not match draft" in error for error in errors))

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
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
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
            source_drafts = drafts / "src-001"
            source_drafts.mkdir()
            (source_drafts / "example.md").write_text(
                "---\nid: example\nsource_id: src-001\nsource_ids: [src-001]\ncandidate_id: candidate-three-way\nstatus: published\npublished_card: example\n---\n",
                encoding="utf-8",
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
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
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
            write_draft(drafts)
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
            write_draft(drafts, source_id="src-002", candidate_id="candidate-other", published_card="", filename="foreign")
            self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_rejects_published_draft_bound_to_raw_only_candidate(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root, candidate_status="raw-only", three_way_assessment="fail")
            write_draft(drafts, status="published")
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
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
            (cards / "example.md").write_text("---\nid: example\nstatus: active\n---\n", encoding="utf-8")
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

    def test_rejects_v1_published_card_without_three_evaluation_tasks(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("exactly three evaluation tasks" in error for error in errors))

    def test_accepts_v1_published_card_with_three_passed_tasks(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            for difficulty in ("typical", "boundary", "anti-pattern"):
                write_evaluation_task(cards, difficulty)
            self.assertEqual([], validator.validate_package(root, drafts, cards))

    def test_rejects_v1_task_with_critical_rubric_failure(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            write_evaluation_task(cards, "typical")
            write_evaluation_task(cards, "boundary", critical_result="fail")
            write_evaluation_task(cards, "anti-pattern")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("critical rubric failure" in error for error in errors))

    def test_rejects_v1_task_without_reviewer_or_response_summary(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            write_evaluation_task(cards, "typical", reviewer="", response_summary="")
            write_evaluation_task(cards, "boundary")
            write_evaluation_task(cards, "anti-pattern")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("reviewer" in error for error in errors))
            self.assertTrue(any("Agent Response Summary" in error for error in errors))

    def test_rejects_v1_task_missing_required_section(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            for difficulty in ("typical", "boundary", "anti-pattern"):
                write_evaluation_task(cards, difficulty)
            task = cards.parent / "eval" / "development-agent" / "example" / "boundary.md"
            task.write_text(
                task.read_text(encoding="utf-8").replace("## Failure Conditions\nFailure.\n\n", ""),
                encoding="utf-8",
            )
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("Failure Conditions" in error for error in errors))

    def test_rejects_v1_card_with_more_than_three_tasks(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "src-001-example"
            drafts = Path(temp_dir) / "drafts"
            cards = Path(temp_dir) / "cards"
            drafts.mkdir()
            cards.mkdir()
            write_package(root)
            write_draft(drafts)
            add_procedure_bindings(drafts)
            write_v1_card(cards)
            for difficulty in ("typical", "boundary", "anti-pattern"):
                write_evaluation_task(cards, difficulty)
            task_dir = cards.parent / "eval" / "development-agent" / "example"
            (task_dir / "extra.md").write_text((task_dir / "typical.md").read_text(encoding="utf-8"), encoding="utf-8")
            errors = validator.validate_package(root, drafts, cards)
            self.assertTrue(any("exactly three evaluation tasks" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
