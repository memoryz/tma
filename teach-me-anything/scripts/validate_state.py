"""Read-only checks for portable tutoring checkpoints; no third-party packages."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


EVIDENCE_TYPES = {
    "recall", "explain", "apply", "predict", "derive", "diagnose", "transfer"
}
MODES = {"diagnostic", "practice", "check", "checkpoint", "review"}
OUTCOMES = {"pass", "partial", "fail", "not_attempted", "invalid"}
STATUSES = {"active", "mitigated", "retention_confirmed"}


def _timestamp(value, label, errors, optional=False):
    if value is None and optional:
        return None
    try:
        if not isinstance(value, str):
            raise ValueError
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError
        return parsed
    except ValueError:
        errors.append(f"{label}: expected a timezone-aware ISO 8601 timestamp")
        return None


def _index(records, label, errors):
    result = {}
    for number, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"{label}[{number}]: expected an object")
            continue
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{label}[{number}]: expected a nonempty string id")
        elif identifier in result:
            errors.append(f"{label}: duplicate id {identifier!r}")
        else:
            result[identifier] = record
    return result


def _reference(value, index, label, errors, optional=False):
    if optional and value is None:
        return
    if not isinstance(value, str) or value not in index:
        errors.append(f"{label}: unknown reference {value!r}")


def _validate_diagnostic(diagnostic, objectives, attempts, updated, errors):
    if "strategy" not in diagnostic:
        return
    if diagnostic["strategy"] != "adaptive_rounds":
        errors.append("diagnostic: unknown strategy")
        return
    initial_errors = len(errors)
    for field, ceiling in (("max_rounds", 5), ("max_questions", 20)):
        if type(diagnostic.get(field)) is not int or not (
            1 <= diagnostic[field] <= ceiling
        ):
            errors.append(f"diagnostic: {field} must be an integer from 1 to {ceiling}")
    if type(diagnostic.get("questions_asked")) is not int or diagnostic["questions_asked"] < 0:
        errors.append("diagnostic: questions_asked must be a nonnegative integer")
    for field in ("rounds", "question_bank"):
        if not isinstance(diagnostic.get(field), list):
            errors.append(f"diagnostic: {field} must be an array")
    if not isinstance(diagnostic.get("status"), str) or diagnostic["status"] not in {
        "not_started", "in_progress", "paused", "complete"
    }:
        errors.append("diagnostic: invalid status")
    if len(errors) != initial_errors:
        return

    if len(diagnostic["rounds"]) > diagnostic["max_rounds"]:
        errors.append("diagnostic: round limit exceeded")
    if diagnostic["questions_asked"] > diagnostic["max_questions"]:
        errors.append("diagnostic: question limit exceeded")
    rounds = _index(diagnostic["rounds"], "diagnostic rounds", errors)
    bank = _index(diagnostic["question_bank"], "diagnostic question_bank", errors)
    presented = set()
    purposes = set()
    question_count = 0
    previous_time = None
    for number, (identifier, round_record) in enumerate(rounds.items()):
        label = f"diagnostic round {identifier}"
        if not isinstance(round_record.get("status"), str) or round_record["status"] not in {
            "in_progress", "complete"
        }:
            errors.append(f"{label}: invalid status")
        elif round_record["status"] == "in_progress" and number != len(rounds) - 1:
            errors.append(f"{label}: only the last round may be in progress")
        reason = round_record.get("selection_reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{label}: selection_reason must be nonempty")
        progression = round_record.get("progression", [])
        if not isinstance(progression, list) or any(
            not isinstance(item, str) or item not in {"harder", "wider", "deeper"}
            for item in progression
        ):
            errors.append(f"{label}: invalid progression")
        elif number > 0 and not progression:
            errors.append(f"{label}: later rounds need harder/wider/deeper progression")
        question_ids = round_record.get("question_ids")
        if not isinstance(question_ids, list):
            errors.append(f"{label}: question_ids must be an array")
            continue
        if not 1 <= len(question_ids) <= 4:
            errors.append(f"{label}: expected one to four presented questions")
        question_count += len(question_ids)
        for question_id in question_ids:
            _reference(question_id, bank, f"{label} question", errors)
            if not isinstance(question_id, str) or question_id not in bank:
                continue
            question_label = f"diagnostic question {question_id}"
            if question_id in presented:
                errors.append(f"{question_label}: presented in multiple round positions")
            presented.add(question_id)
            question = bank[question_id]
            _reference(
                question.get("objective_id"), objectives,
                f"{question_label} objective", errors,
            )
            at = _timestamp(question.get("asked_at"), f"{question_label} asked_at", errors)
            if at is not None:
                if previous_time is not None and at < previous_time:
                    errors.append(f"{question_label}: exposures must be chronological")
                previous_time = at
            for field in ("diagnostic_purpose", "placement_effect"):
                if not isinstance(question.get(field), str) or not question[field].strip():
                    errors.append(f"{question_label}: {field} must be nonempty")
            purpose = question.get("diagnostic_purpose")
            if isinstance(purpose, str) and purpose.strip():
                normalized = " ".join(purpose.casefold().split())
                if normalized in purposes:
                    errors.append(f"{question_label}: duplicate diagnostic purpose")
                purposes.add(normalized)
    if question_count != diagnostic["questions_asked"]:
        errors.append("diagnostic: questions_asked must match all presented round questions")
    if question_count > diagnostic["max_questions"]:
        errors.append("diagnostic: presented questions exceed the question limit")
    if previous_time is not None and (updated is None or updated < previous_time):
        errors.append("updated_at: must cover the latest diagnostic question")
    for question_id, question in bank.items():
        if question.get("asked_at") is not None and question_id not in presented:
            errors.append(f"diagnostic question {question_id}: exposure missing from rounds")
    if diagnostic["status"] == "not_started" and question_count:
        errors.append("diagnostic: not_started cannot contain presented questions")
    if diagnostic["status"] == "complete":
        reason = diagnostic.get("stop_reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("diagnostic: completed placement needs a stop_reason")
    for attempt in attempts:
        if isinstance(attempt, dict) and attempt.get("mode") == "diagnostic":
            question_id = attempt.get("diagnostic_question_id")
            _reference(
                question_id, bank,
                f"attempt {attempt.get('id')}: diagnostic_question_id", errors,
            )
            if isinstance(question_id, str) and question_id in bank and question_id not in presented:
                errors.append(f"attempt {attempt.get('id')}: diagnostic question was not presented")


def _replay(weakness, attempts, errors):
    recent = []
    mitigated = False
    retained = False
    mitigation_session = None
    used_tasks = set()
    required = set(weakness["required_evidence_types"])
    for attempt in attempts:
        if attempt["weakness_id"] != weakness["id"]:
            continue
        if attempt["mode"] == "practice" or attempt["outcome"] in {
            "not_attempted", "invalid"
        }:
            continue
        label = f"attempt {attempt['id']}"
        if attempt["task_id"] in used_tasks:
            errors.append(f"{label}: repeated scored task for {weakness['id']}")
        used_tasks.add(attempt["task_id"])
        if attempt["retention_check"]:
            if not mitigated:
                errors.append(f"{label}: retention_check requires earlier mitigation")
            elif attempt["session_id"] == mitigation_session:
                errors.append(f"{label}: retention_check must be in a later session")
        if attempt["outcome"] != "pass" or not attempt["independent"]:
            recent = []
            mitigated = retained = False
            mitigation_session = None
            continue
        was_mitigated = mitigated
        recent = (recent + [attempt["evidence_type"]])[-3:]
        if not mitigated and len(recent) == 3 and required.issubset(recent):
            mitigated = True
            mitigation_session = attempt["session_id"]
        if was_mitigated and attempt["retention_check"]:
            retained = True
    status = "retention_confirmed" if retained else (
        "mitigated" if mitigated else "active"
    )
    for field, expected in (("success_streak", len(recent)), ("status", status)):
        if weakness[field] != expected:
            errors.append(
                f"weakness {weakness['id']}: {field} is {weakness[field]!r}; "
                f"evidence requires {expected!r}"
            )


def validate_state(state):
    """Return consistency errors without changing state or evaluating answers."""
    errors = []
    if not isinstance(state, dict):
        return ["state: expected a JSON object"]
    if type(state.get("format_version")) is not int or state["format_version"] != 1:
        errors.append("format_version: expected 1")
    for field in ("goal", "diagnostic", "resume"):
        if not isinstance(state.get(field), dict):
            errors.append(f"{field}: expected an object")
    for field in (
        "sources", "objectives", "phases", "sessions", "attempts", "weaknesses",
        "review_queue",
    ):
        if not isinstance(state.get(field), list):
            errors.append(f"{field}: expected an array")
    if "topic" not in state or (
        state["topic"] is not None and not isinstance(state["topic"], str)
    ):
        errors.append("topic: expected a string or null")
    if "updated_at" not in state:
        errors.append("updated_at: missing")
    if errors:
        return errors

    updated = _timestamp(state["updated_at"], "updated_at", errors, optional=True)
    objectives = _index(state["objectives"], "objectives", errors)
    phases = _index(state["phases"], "phases", errors)
    sessions = _index(state["sessions"], "sessions", errors)
    weaknesses = _index(state["weaknesses"], "weaknesses", errors)
    _index(state["sources"], "sources", errors)
    _index(state["attempts"], "attempts", errors)
    _validate_diagnostic(state["diagnostic"], objectives, state["attempts"], updated, errors)
    session_times = {}
    for identifier, session in sessions.items():
        start = _timestamp(session.get("started_at"), f"session {identifier}", errors)
        end = _timestamp(
            session.get("ended_at"), f"session {identifier} end", errors, optional=True
        )
        if start is not None and end is not None and end < start:
            errors.append(f"session {identifier}: end precedes start")
        minutes = session.get("available_minutes")
        if minutes is not None and (
            type(minutes) not in (int, float) or minutes <= 0
        ):
            errors.append(f"session {identifier}: available_minutes must be positive or null")
        session_times[identifier] = (start, end)

    for identifier, objective in objectives.items():
        prerequisites = objective.get("prerequisite_ids", [])
        if not isinstance(prerequisites, list):
            errors.append(f"objective {identifier}: prerequisite_ids must be an array")
            continue
        for prerequisite in prerequisites:
            _reference(prerequisite, objectives, f"objective {identifier} prerequisite", errors)
            if prerequisite == identifier:
                errors.append(f"objective {identifier}: cannot depend on itself")
    for identifier, phase in phases.items():
        members = phase.get("objective_ids", [])
        if not isinstance(members, list):
            errors.append(f"phase {identifier}: objective_ids must be an array")
            continue
        for objective in members:
            _reference(objective, objectives, f"phase {identifier} objective", errors)
    for identifier, weakness in weaknesses.items():
        label = f"weakness {identifier}"
        _reference(weakness.get("objective_id"), objectives, label, errors)
        evidence = weakness.get("required_evidence_types")
        if not isinstance(evidence, list) or not evidence or any(
            not isinstance(item, str) or item not in EVIDENCE_TYPES for item in evidence
        ):
            errors.append(f"{label}: expected nonempty required_evidence_types")
        if type(weakness.get("success_streak")) is not int or not (
            0 <= weakness["success_streak"] <= 3
        ):
            errors.append(f"{label}: success_streak must be an integer from 0 to 3")
        if not isinstance(weakness.get("status"), str) or weakness["status"] not in STATUSES:
            errors.append(f"{label}: invalid status")

    previous_time = None
    for number, attempt in enumerate(state["attempts"]):
        if not isinstance(attempt, dict):
            continue
        label = f"attempt {attempt.get('id', number)}"
        _reference(attempt.get("session_id"), sessions, f"{label} session", errors)
        _reference(attempt.get("objective_id"), objectives, f"{label} objective", errors)
        _reference(
            attempt.get("weakness_id"), weaknesses, f"{label} weakness", errors,
            optional=True,
        )
        if "weakness_id" not in attempt:
            errors.append(f"{label}: weakness_id must be a reference or null")
        weakness = weaknesses.get(attempt.get("weakness_id")) if isinstance(
            attempt.get("weakness_id"), str
        ) else None
        if weakness and weakness.get("objective_id") != attempt.get("objective_id"):
            errors.append(f"{label}: weakness belongs to a different objective")
        for field in ("task_id", "prompt", "rubric"):
            if not isinstance(attempt.get(field), str) or not attempt[field].strip():
                errors.append(f"{label}: {field} must be a nonempty string")
        for field in ("response", "feedback", "retention_basis"):
            if not isinstance(attempt.get(field), str):
                errors.append(f"{label}: {field} must be a string")
        for field in ("independent", "retention_check"):
            if type(attempt.get(field)) is not bool:
                errors.append(f"{label}: {field} must be a boolean")
        for field, choices in (
            ("mode", MODES), ("outcome", OUTCOMES), ("evidence_type", EVIDENCE_TYPES)
        ):
            if not isinstance(attempt.get(field), str) or attempt[field] not in choices:
                errors.append(f"{label}: invalid {field}")
        if attempt.get("retention_check") is True:
            if attempt.get("mode") != "review" or not attempt.get("weakness_id"):
                errors.append(f"{label}: retention_check needs a review and a weakness")
            if not isinstance(attempt.get("retention_basis"), str) or not (
                attempt["retention_basis"].strip()
            ):
                errors.append(f"{label}: retention_check needs a retention_basis")
        at = _timestamp(attempt.get("at"), f"{label} at", errors)
        if at is not None:
            if previous_time is not None and at < previous_time:
                errors.append(f"{label}: attempts must be chronological")
            previous_time = at
            times = session_times.get(attempt.get("session_id")) if isinstance(
                attempt.get("session_id"), str
            ) else None
            if times is not None:
                start, end = times
                if start is not None and at < start:
                    errors.append(f"{label}: precedes its session")
                if end is not None and at > end:
                    errors.append(f"{label}: follows its session")
    if previous_time is not None and (updated is None or updated < previous_time):
        errors.append("updated_at: must cover the latest attempt")
    _reference(state["resume"].get("phase_id"), phases, "resume phase", errors, optional=True)
    _reference(
        state["resume"].get("objective_id"), objectives, "resume objective", errors,
        optional=True,
    )
    if errors:
        return errors
    for weakness in weaknesses.values():
        _replay(weakness, state["attempts"], errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="Path to learner-state.json")
    args = parser.parse_args()
    try:
        state = json.loads(args.state.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        print(f"Cannot read checkpoint: {error}", file=sys.stderr)
        return 1
    errors = validate_state(state)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Checkpoint bookkeeping is consistent; answer quality was not evaluated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
