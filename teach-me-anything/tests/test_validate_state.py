import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_state", ROOT / "scripts" / "validate_state.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def initial_state():
    return json.loads((ROOT / "templates" / "learner-state.json").read_text("utf-8"))


def learning_state():
    state = initial_state()
    state["topic"] = "Synthetic probability example"
    state["objectives"] = [
        {"id": "o1", "description": "Explain and apply conditioning.", "prerequisite_ids": []},
        {"id": "o2", "description": "Describe independence.", "prerequisite_ids": []},
    ]
    state["weaknesses"] = [{
        "id": "w1",
        "objective_id": "o1",
        "description": "Reverses the condition.",
        "required_evidence_types": ["explain", "apply"],
        "success_streak": 0,
        "status": "active",
    }]
    state["sessions"] = [
        {
            "id": f"s{number}",
            "started_at": timestamp,
            "ended_at": None,
            "available_minutes": 15,
        }
        for number, timestamp in enumerate((
            "2026-01-05T18:00:00+00:00",
            "2026-04-05T18:00:00+00:00",
            "2026-10-05T18:00:00+00:00",
        ), start=1)
    ]
    return state


def add_attempt(state, **changes):
    number = len(state["attempts"]) + 1
    attempt = {
        "id": f"a{number}",
        "session_id": "s1",
        "objective_id": "o1",
        "weakness_id": "w1",
        "task_id": f"t{number}",
        "mode": "check",
        "outcome": "pass",
        "independent": True,
        "evidence_type": "explain" if number % 2 else "apply",
        "retention_check": False,
        "retention_basis": "",
        "prompt": f"Synthetic distinct task {number}.",
        "response": "Synthetic learner response.",
        "rubric": "Explain the conditioning event and apply it correctly.",
        "feedback": "",
    }
    attempt.update(changes)
    session = next(item for item in state["sessions"] if item["id"] == attempt["session_id"])
    attempt.setdefault(
        "at",
        (datetime.fromisoformat(session["started_at"]) + timedelta(seconds=number)).isoformat(),
    )
    state["attempts"].append(attempt)
    state["updated_at"] = attempt["at"]
    return attempt


def set_summary(state, streak, status):
    state["weaknesses"][0].update(success_streak=streak, status=status)


def mitigate(state):
    for evidence_type in ("explain", "apply", "predict"):
        add_attempt(state, evidence_type=evidence_type)
    set_summary(state, 3, "mitigated")


class BookkeepingTests(unittest.TestCase):
    def assert_valid(self, state):
        self.assertEqual(VALIDATOR.validate_state(state), [])

    def test_empty_template_is_valid(self):
        self.assert_valid(initial_state())

    def test_successes_can_span_irregular_month_long_gaps(self):
        state = learning_state()
        for session in ("s1", "s2", "s3"):
            add_attempt(state, session_id=session)
        set_summary(state, 3, "mitigated")
        self.assert_valid(state)

    def test_elapsed_time_does_not_change_mastery(self):
        state = learning_state()
        mitigate(state)
        state["updated_at"] = "2030-12-01T00:00:00+00:00"
        self.assert_valid(state)
        set_summary(state, 0, "active")
        self.assertTrue(VALIDATOR.validate_state(state))

    def test_scored_failure_partial_or_assistance_resets_the_run(self):
        for changes in (
            {"outcome": "fail"},
            {"outcome": "partial"},
            {"independent": False},
        ):
            with self.subTest(changes=changes):
                state = learning_state()
                add_attempt(state)
                add_attempt(state)
                add_attempt(state, **changes)
                add_attempt(state)
                set_summary(state, 1, "active")
                self.assert_valid(state)

    def test_practice_and_excluded_attempts_do_not_reset_the_run(self):
        state = learning_state()
        add_attempt(state, evidence_type="explain")
        add_attempt(state, mode="practice", outcome="fail", independent=False)
        add_attempt(state, outcome="not_attempted", independent=False)
        add_attempt(state, outcome="invalid")
        add_attempt(state, evidence_type="apply")
        add_attempt(state, evidence_type="predict")
        set_summary(state, 3, "mitigated")
        self.assert_valid(state)

    def test_unrelated_failure_does_not_reset_a_weakness(self):
        state = learning_state()
        add_attempt(state, evidence_type="explain")
        add_attempt(state, objective_id="o2", weakness_id=None, outcome="fail")
        add_attempt(state, evidence_type="apply")
        set_summary(state, 2, "active")
        self.assert_valid(state)

    def test_same_task_cannot_supply_multiple_scored_successes(self):
        state = learning_state()
        add_attempt(state, task_id="repeated")
        add_attempt(state, task_id="repeated")
        set_summary(state, 2, "active")
        self.assertTrue(any(
            "repeated scored task" in error for error in VALIDATOR.validate_state(state)
        ))

    def test_interrupted_task_can_later_have_one_submitted_judgment(self):
        state = learning_state()
        add_attempt(state, task_id="unfinished", outcome="not_attempted")
        add_attempt(state, task_id="unfinished", session_id="s2")
        set_summary(state, 1, "active")
        self.assert_valid(state)

    def test_required_evidence_variety_is_needed_for_mitigation(self):
        state = learning_state()
        for _ in range(3):
            add_attempt(state, evidence_type="explain")
        set_summary(state, 3, "active")
        self.assert_valid(state)
        set_summary(state, 3, "mitigated")
        self.assertTrue(VALIDATOR.validate_state(state))
        add_attempt(state, evidence_type="apply")
        self.assert_valid(state)

    def test_further_successes_do_not_remove_earned_mitigation(self):
        state = learning_state()
        mitigate(state)
        for _ in range(4):
            add_attempt(state, evidence_type="recall")
        self.assert_valid(state)

    def test_later_independent_review_confirms_retention(self):
        state = learning_state()
        mitigate(state)
        add_attempt(
            state, session_id="s2", mode="review", retention_check=True,
            retention_basis="Three months later, before any recap or hint.",
        )
        set_summary(state, 3, "retention_confirmed")
        self.assert_valid(state)

    def test_mitigation_and_retention_cannot_be_established_by_one_check(self):
        state = learning_state()
        add_attempt(state)
        add_attempt(state)
        add_attempt(
            state, session_id="s2", mode="review", retention_check=True,
            retention_basis="Later session, but not previously mitigated.",
        )
        set_summary(state, 3, "mitigated")
        self.assertTrue(any(
            "earlier mitigation" in error for error in VALIDATOR.validate_state(state)
        ))

    def test_same_session_review_cannot_confirm_delayed_retention(self):
        state = learning_state()
        mitigate(state)
        add_attempt(
            state, mode="review", retention_check=True,
            retention_basis="Same session is not delayed evidence.",
        )
        set_summary(state, 3, "retention_confirmed")
        self.assertTrue(any(
            "later session" in error for error in VALIDATOR.validate_state(state)
        ))

    def test_review_failure_or_assistance_reopens_the_gap(self):
        for changes in ({"outcome": "fail"}, {"independent": False}):
            with self.subTest(changes=changes):
                state = learning_state()
                mitigate(state)
                add_attempt(
                    state, session_id="s2", mode="review", retention_check=True,
                    retention_basis="A later session before instruction.", **changes,
                )
                set_summary(state, 0, "active")
                self.assert_valid(state)

    def test_failure_after_retention_preserves_history_but_reopens_gap(self):
        state = learning_state()
        mitigate(state)
        add_attempt(
            state, session_id="s2", mode="review", retention_check=True,
            retention_basis="A later session before instruction.",
        )
        add_attempt(state, session_id="s3", mode="review", outcome="fail")
        set_summary(state, 0, "active")
        self.assert_valid(state)
        self.assertEqual(len(state["attempts"]), 5)

    def test_invalidated_grading_is_replayed_without_penalty(self):
        state = learning_state()
        mitigate(state)
        mistaken = add_attempt(state, outcome="fail")
        mistaken.update(outcome="invalid", feedback="Tutor grading was incorrect.")
        self.assert_valid(state)

    def test_bad_references_and_cross_objective_judgments_are_rejected(self):
        for field, value in (
            ("session_id", "missing"),
            ("weakness_id", "missing"),
            ("objective_id", "o2"),
        ):
            with self.subTest(field=field):
                state = learning_state()
                attempt = add_attempt(state)
                attempt[field] = value
                self.assertTrue(VALIDATOR.validate_state(state))

    def test_out_of_order_or_naive_timestamps_are_rejected(self):
        for at in ("2025-01-01T00:00:00+00:00", "2026-01-05T18:05:00"):
            with self.subTest(at=at):
                state = learning_state()
                add_attempt(state)
                add_attempt(state, at=at)
                self.assertTrue(VALIDATOR.validate_state(state))

    def test_malformed_records_return_errors_instead_of_crashing(self):
        for value in (None, [], "not an object"):
            with self.subTest(value=value):
                self.assertTrue(VALIDATOR.validate_state(value))
        for field, value in (
            ("independent", "yes"), ("mode", []), ("outcome", None),
            ("session_id", []), ("weakness_id", {}),
        ):
            with self.subTest(field=field):
                state = learning_state()
                attempt = add_attempt(state)
                attempt[field] = value
                self.assertTrue(VALIDATOR.validate_state(state))

    def test_validation_does_not_mutate_records(self):
        state = learning_state()
        mitigate(state)
        before = copy.deepcopy(state)
        self.assert_valid(state)
        self.assertEqual(state, before)


class AdaptivePlacementTests(unittest.TestCase):
    def add_question(self, state, round_record):
        diagnostic = state["diagnostic"]
        number = len(diagnostic["question_bank"]) + 1
        at = (
            datetime.fromisoformat(state["sessions"][0]["started_at"])
            + timedelta(seconds=number)
        ).isoformat()
        question = {
            "id": f"q{number}",
            "objective_id": "o1",
            "asked_at": at,
            "diagnostic_purpose": f"Distinguish conditioning misconception {number}.",
            "placement_effect": f"Select the starting explanation for subcase {number}.",
            "prompt": f"Synthetic distinct diagnostic demand {number}.",
            "rubric": "Identify and justify the conditioning population.",
            "response": None,
        }
        diagnostic["question_bank"].append(question)
        diagnostic["questions_asked"] += 1
        round_record["question_ids"].append(question["id"])
        state["updated_at"] = at
        return question

    def add_round(self, state, count=1, progression=None):
        diagnostic = state["diagnostic"]
        if diagnostic["rounds"]:
            diagnostic["rounds"][-1]["status"] = "complete"
        number = len(diagnostic["rounds"]) + 1
        round_record = {
            "id": f"r{number}",
            "status": "in_progress",
            "progression": (
                progression if progression is not None
                else ([] if number == 1 else ["deeper"])
            ),
            "selection_reason": f"Resolve the next uncertain boundary in cycle {number}.",
            "question_ids": [],
        }
        diagnostic["rounds"].append(round_record)
        diagnostic["status"] = "in_progress"
        for _ in range(count):
            self.add_question(state, round_record)
        return round_record

    def assert_valid(self, state):
        self.assertEqual(VALIDATOR.validate_state(state), [])

    def assert_error(self, state, fragment):
        self.assertTrue(
            any(fragment in error for error in VALIDATOR.validate_state(state)),
            VALIDATOR.validate_state(state),
        )

    def test_caps_are_not_minimums_and_early_stopping_is_valid(self):
        for count in (0, 1, 3):
            with self.subTest(count=count):
                state = learning_state()
                if count:
                    self.add_round(state, count=count)["status"] = "complete"
                state["diagnostic"].update(
                    status="complete", stop_reason="Profile sufficient or learner declined."
                )
                self.assert_valid(state)

    def test_exact_five_round_twenty_question_boundary_is_valid(self):
        state = learning_state()
        for _ in range(5):
            self.add_round(state, count=4)
        self.assert_valid(state)

    def test_round_question_and_per_round_limits_are_enforced(self):
        state = learning_state()
        for _ in range(6):
            self.add_round(state)
        self.assert_error(state, "round limit exceeded")
        state = learning_state()
        self.add_round(state, count=5)
        self.assert_error(state, "one to four")
        state = learning_state()
        state["diagnostic"]["max_questions"] = 3
        self.add_round(state, count=4)
        self.assert_error(state, "question limit")

    def test_limits_may_be_lowered_but_not_raised_or_mistyped(self):
        state = learning_state()
        state["diagnostic"].update(max_rounds=1, max_questions=2)
        self.add_round(state, count=2)
        self.assert_valid(state)
        for field, value in (
            ("max_rounds", 6), ("max_questions", 21),
            ("max_rounds", True), ("max_questions", 0),
        ):
            with self.subTest(field=field, value=value):
                state = learning_state()
                state["diagnostic"][field] = value
                self.assert_error(state, field)

    def test_each_later_round_needs_harder_wider_or_deeper_progression(self):
        state = learning_state()
        self.add_round(state)
        later = self.add_round(state, progression=[])
        self.assert_error(state, "progression")
        for progression in (["harder"], ["wider"], ["deeper"], ["wider", "deeper"]):
            with self.subTest(progression=progression):
                later["progression"] = progression
                self.assert_valid(state)
        later["progression"] = ["repeat"]
        self.assert_error(state, "invalid progression")

    def test_question_purposes_must_be_present_and_textually_distinct(self):
        state = learning_state()
        self.add_round(state, count=2)
        first, second = state["diagnostic"]["question_bank"]
        second["diagnostic_purpose"] = "  " + first["diagnostic_purpose"].upper() + "  "
        self.assert_error(state, "duplicate diagnostic purpose")
        for field in ("diagnostic_purpose", "placement_effect"):
            with self.subTest(field=field):
                state = learning_state()
                self.add_round(state)
                state["diagnostic"]["question_bank"][0][field] = ""
                self.assert_error(state, field)

    def test_unanswered_and_invalid_exposures_still_use_the_budget(self):
        state = learning_state()
        self.add_round(state, count=3)
        bank = state["diagnostic"]["question_bank"]
        bank[0]["response"] = None
        bank[1]["screening_outcome"] = "invalid"
        bank[2]["response"] = "A"
        self.assert_valid(state)
        state["diagnostic"]["questions_asked"] = 1
        self.assert_error(state, "must match all presented")

    def test_unused_candidates_are_free_but_unlogged_exposures_are_rejected(self):
        state = learning_state()
        self.add_round(state)
        candidate = copy.deepcopy(state["diagnostic"]["question_bank"][0])
        candidate.update(id="unasked", asked_at=None)
        state["diagnostic"]["question_bank"].append(candidate)
        self.assert_valid(state)
        candidate["asked_at"] = state["updated_at"]
        self.assert_error(state, "exposure missing from rounds")

    def test_pause_resume_preserves_round_and_followup_budget(self):
        state = learning_state()
        state["diagnostic"]["max_questions"] = 3
        round_record = self.add_round(state, count=2)
        state["diagnostic"]["status"] = "paused"
        before = copy.deepcopy(state)
        self.assert_valid(state)
        self.assertEqual(state, before)
        state["diagnostic"]["status"] = "in_progress"
        self.add_question(state, round_record)
        self.assert_valid(state)
        self.assertEqual(len(state["diagnostic"]["rounds"]), 1)
        self.add_question(state, round_record)
        self.assert_error(state, "question limit")

    def test_round_question_references_cannot_be_reused_or_dropped(self):
        state = learning_state()
        first = self.add_round(state)
        second = self.add_round(state)
        second["question_ids"][0] = first["question_ids"][0]
        self.assert_error(state, "multiple round positions")
        second["question_ids"][0] = "unknown"
        self.assert_error(state, "unknown reference")

    def test_scored_diagnostic_attempt_links_to_a_presented_question(self):
        state = learning_state()
        self.add_round(state)
        attempt = add_attempt(state, mode="diagnostic", weakness_id=None)
        self.assert_error(state, "diagnostic_question_id")
        attempt["diagnostic_question_id"] = "q1"
        self.assert_valid(state)

    def test_legacy_diagnostic_records_remain_readable_without_reset(self):
        state = learning_state()
        state["diagnostic"] = {
            "status": "in_progress", "target_questions": 15,
            "questions_asked": 12, "question_bank": [],
        }
        before = copy.deepcopy(state)
        self.assert_valid(state)
        self.assertEqual(state, before)

    def test_malformed_adaptive_records_return_errors_and_completion_needs_a_reason(self):
        for field, value in (
            ("rounds", {}), ("question_bank", None), ("questions_asked", True),
            ("strategy", []), ("status", []),
        ):
            with self.subTest(field=field):
                state = learning_state()
                state["diagnostic"][field] = value
                self.assertTrue(VALIDATOR.validate_state(state))
        state = learning_state()
        self.add_round(state)
        state["diagnostic"]["status"] = "complete"
        self.assert_error(state, "stop_reason")


class PackageTests(unittest.TestCase):
    def test_skill_frontmatter_and_name_match_the_portable_folder(self):
        text = (ROOT / "SKILL.md").read_text("utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        name = re.search(r"^name: (.+)$", frontmatter, re.MULTILINE).group(1)
        description = re.search(
            r"^description: (.+)$", frontmatter, re.MULTILINE
        ).group(1)
        self.assertEqual(name, ROOT.name)
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertTrue(0 < len(description) <= 1024)
        self.assertLess(len(text.splitlines()), 500)

    def test_local_markdown_links_resolve_inside_the_package(self):
        links_checked = 0
        for document in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text("utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                resolved = (document.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.is_file())
                links_checked += 1
        self.assertGreater(links_checked, 0)

    def test_command_reports_a_valid_checkpoint_without_modifying_it(self):
        template = ROOT / "templates" / "learner-state.json"
        before = template.read_bytes()
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "validate_state.py"), str(template)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(template.read_bytes(), before)

    def test_command_reports_invalid_json_and_inconsistent_bookkeeping(self):
        with tempfile.TemporaryDirectory(prefix="teach-me-anything-test-") as directory:
            checkpoint = Path(directory) / "learner-state.json"
            inconsistent = learning_state()
            set_summary(inconsistent, 3, "mitigated")
            for content in ("{broken json", json.dumps(inconsistent)):
                with self.subTest(content=content[:30]):
                    checkpoint.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [
                            sys.executable, "-B",
                            str(ROOT / "scripts" / "validate_state.py"), str(checkpoint),
                        ],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertTrue(result.stderr)
                    self.assertEqual(checkpoint.read_text("utf-8"), content)


if __name__ == "__main__":
    unittest.main()
