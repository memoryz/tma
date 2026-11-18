# State, persistence, and irregular sessions

## Files and authority

Create a separate learner/topic workspace from the templates. Never edit the
templates to store a real learner's progress. Keep these records portable:

- `learner-state.json`: authoritative structured evidence and resume position.
- `roadmap.md`: readable scope, sources, concept map, phases, and rubrics.
- `progress.md`: readable strengths, specific gaps, and next action.
- `capstone-brief.md` and `capstone-assessment.md`, created when needed: the
  learner-facing case and separate assessor mapping, rubric, and interview notes.

Do not assume cross-session memory, file access, or a background process.
If files cannot be written, state that limitation and provide an exportable
checkpoint. If a save fails, preserve the current records and do not claim success.
Use safe replacement or an equivalent host facility, avoiding partial JSON writes.
Do not overwrite a newer checkpoint when multiple conversations share a workspace.

Save after each scored judgment and meaningful teaching segment. Resume from the
last durable checkpoint rather than inventing answers from a missing transcript.

## State fields and compatibility

Start with `templates/learner-state.json`. Keep its top-level keys; additional
fields are allowed. Use actual timezone-aware ISO 8601 timestamps, not invented
dates. `updated_at` and `topic` may be null before the first session.

| Field | Meaning |
| --- | --- |
| `format_version` | Currently `1`. |
| `topic` | Scoped topic title, or null before intake. |
| `goal` | Practical use, target capabilities, focus, background, constraints, and interaction preferences. |
| `sources` | Source IDs, titles, URLs or bibliographic references, version/date notes. |
| `concepts` | Unique concept IDs, titles, required/optional and scope status, and linked objective IDs; used for roadmap counts. |
| `objectives` | IDs, descriptions, depth/evidence requirements, prerequisites, rubrics, required/optional status. |
| `phases` | IDs, objective IDs, mental-model notes, exit rubrics, status, historical gate evidence and bypasses. |
| `diagnostic` | Adaptive strategy, round/question caps and exposure log, progression decisions, coverage profile, stop reason, saved questions and criteria, instruction notes, and unsampled objective IDs. |
| `sessions` | Session IDs, actual start/end times, available minutes, notes, and session wrap-up summaries. |
| `attempts` | Chronological judgments with actual responses and assistance. |
| `weaknesses` | Specific gaps and derived streak/status summaries. |
| `review_queue` | Suggested checks, priorities, and optional soft date hints. |
| `capstone` | Optional final-interview plan, selected targets, material references, status, and evidence IDs; null before planning. |
| `resume` | Current stage, phase/objective, pending follow-up choice, unfinished task, next action. |
| `updated_at` | Last successful checkpoint timestamp. |

`goal.focus` is null until chosen, then `breadth`, `depth`, or `mixed`.
Each saved diagnostic question needs an ID, objective ID, diagnostic purpose,
evidence type, task ID, prompt, reference answer or rubric, and related attempt
IDs. Keep answer criteria out of the learner-facing presentation before attempts.
For option-based questions, also save stable option IDs and labels. Keep the
answer key separate from the displayed choices. Store choice-only screening
responses with the question rather than inventing mastery judgments.
Record instruction and hints in `diagnostic.instruction_notes` so later answers
are not mislabeled as untaught placement evidence. Save revisions to the bank
as the assessment adapts.

### Adaptive diagnostic records

New assessments use `strategy: "adaptive_rounds"`, `max_rounds: 5`, and
`max_questions: 20`. Limits may be lowered, never silently raised. There is no
target or minimum count. The `status` is `not_started`, `in_progress`, `paused`,
or `complete`; save a nonempty `stop_reason` when complete.

The `rounds` list contains only rounds that have actually started. Each round
has an ID, `status` (`in_progress` or `complete`), `selection_reason`, and
`question_ids` in presentation order. One to four question IDs belong to each
round, and each presented question belongs to exactly one round. The first
round establishes a baseline; every subsequent round needs a nonempty
`progression` list containing `harder`, `wider`, or `deeper`, with a reason
grounded in earlier responses. Save observations and the next decision as well.

```json
{
  "id": "round-002",
  "status": "in_progress",
  "progression": ["deeper"],
  "selection_reason": "Check whether correct vocabulary extends to choosing the conditioning population.",
  "question_ids": ["question-conditioning-population"],
  "observations": "",
  "next_decision": null
}
```

In the saved `question_bank`, each actually presented question has an `asked_at`
timestamp, a distinct `diagnostic_purpose`, and a `placement_effect` explaining
how its answer could change instruction. Save its prompt, options, criterion,
and response as already specified. A purpose describes a distinct uncertainty
or contrast, not merely "question 3" or a rewording of a settled inference.
Later reasoning follow-ups get their own question IDs and consume budget.
Unasked candidates have `asked_at: null` and consume no budget.

Derive `questions_asked` from the question IDs in all started rounds, not the
number of answers, scored judgments, or correct responses. Invalid and unattempted
presented questions still count. Never remove an exposure to reclaim capacity.
Resuming the same unfinished prompt retains its ID and original exposure.
A scored attempt with `mode: "diagnostic"` links back through
`diagnostic_question_id`; choice-only screening responses remain in the question
record rather than earning mastery credit.

Store per-branch strengths, independent depth boundaries, confirmed/tentative
gaps, relevant question or attempt IDs, and uncertainty in `coverage_profile`.
Use `unsampled_objective_ids` for unknown coverage. An unanswered advanced
question is not evidence that the learner lacks every prerequisite.

Save and check the same round and question counters across sessions. A paused
placement resumes its existing round, not a new five-round allowance. Once a
cap is reached, finish the profile with explicit unknowns; do not extend the
survey or disguise more placement questions as practice.

Legacy checkpoints without `strategy` remain readable. Preserve their historical
`questions_asked`; the old `target_questions` is not a minimum or a fresh budget.
Reconstruct rounds only from reliable saved evidence. If the remaining allowance
cannot be established, end placement with a provisional profile rather than
inventing round history or granting five more rounds. Do not modify real learner
records merely to update this skill.

`goal.interaction_preferences` records expressed preferences, not fixed learner
types. Default to `practice_pacing: "offer_followup"` and `diagrams: "when_helpful"`.
If the learner requests continuous practice, record that pacing preference so
the tutor does not re-ask before every scenario. They can change it at any time.

The concept inventory, interaction preferences, pending choice, and session
summaries are additive metadata in format version 1. Older checkpoints remain
usable: a missing pending choice is null, missing preferences use the defaults,
and missing concept totals stay unknown until reconstructed from the agreed
roadmap. Never reset evidence or invent an inventory during this update.

### Capstone records

The optional `capstone` is also additive format-version-1 metadata. A missing
field is equivalent to null, not a reason to migrate or reset an older checkpoint.
Create the brief and assessor record from their templates only when needed, in
the learner's workspace rather than the reusable skill package. Keep answer
criteria out of the brief and upcoming learner-facing progress notes.

When planned, record:

| Field | Meaning |
| --- | --- |
| `id` | Stable capstone identifier. |
| `task_id` | Original scenario's task ID, shared by its per-target judgments. |
| `status` | `planned`, `in_progress`, `paused`, `passed`, `needs_repair`, or `deferred`. |
| `eligible_gap_count` | Distinct eligible learned gaps at selection, used to explain the coverage count. |
| `target_weakness_ids` | At least three distinct eligible IDs when available, otherwise all one or two; empty only for an objective-based case. |
| `target_objective_ids` | Existing objective IDs actually assessed, including any objective-only targets. |
| `selection_snapshot` | Each target's status and supporting attempt IDs at selection, plus why it was chosen. |
| `brief_file`, `assessment_file` | Workspace-relative material references, or saved text when files are unavailable. |
| `attempt_ids` | Authoritative judgment references, including later fresh retests when needed. |

Keep the exact pending interviewer prompt, data already supplied, partial learner
reasoning, resources, and assistance under `resume.pending_task` and in the
interview notes. The resume task must retain the original task ID across sessions.
Save interim turns without prematurely grading a partially completed target.
Once a target is submitted for judgment, record at most one scored attempt for
that weakness on that task, using `mode: "checkpoint"` and an appropriate evidence
type such as `transfer`. Different targets can have different independence flags.
Objective-only targets link their objective and use `weakness_id: null`; never
invent a weakness merely to record successful evidence.
Use new task IDs for genuinely fresh retests, not for resumed turns or retries.

The structured attempts remain authoritative for streaks and current gap status;
the assessor record preserves scenario context, indicative solutions, and notes.
Do not delete the original selection snapshot, failed case, or earlier evidence
when a target needs repair. Keep later versions and retest references auditable.
A passed capstone requires independent evidence for the overall case and every
selected target, with no unmet required learning gate hidden by the result.
Neither completing all phases nor simply finishing the interview implies a pass.
Use the existing session summaries to connect capstone work to roadmap progress.

## Core record shapes

Use stable, unique IDs. These are illustrative synthetic fragments, not starter
learner data:

```json
{
  "id": "concept-conditional-probability",
  "title": "Conditional probability",
  "required": true,
  "scope_status": "in_scope",
  "objective_ids": ["objective-conditional-probability"]
}
```

For concepts, `scope_status` is `in_scope`, `deferred`, or `out_of_scope`.
Keep scope changes explicit; a previously required but now deferred concept is
not part of the current required denominator.

```json
{
  "id": "objective-conditional-probability",
  "description": "Distinguish a conditional probability from its reverse.",
  "required": true,
  "prerequisite_ids": [],
  "required_evidence_types": ["explain", "apply"],
  "rubric": "State the conditioning event and reason with the correct population."
}
```

```json
{
  "id": "session-001",
  "started_at": "2026-01-05T18:00:00+00:00",
  "ended_at": null,
  "available_minutes": 15,
  "notes": ""
}
```

Each attempt is one judgment for one objective and, optionally, one weakness:

```json
{
  "id": "attempt-001",
  "session_id": "session-001",
  "objective_id": "objective-conditional-probability",
  "weakness_id": "weakness-reversed-conditioning",
  "task_id": "task-new-base-rate-scenario",
  "at": "2026-01-05T18:07:00+00:00",
  "mode": "check",
  "outcome": "fail",
  "independent": true,
  "evidence_type": "apply",
  "retention_check": false,
  "retention_basis": "",
  "prompt": "The actual question, including permitted resources.",
  "response": "The actual learner response, not an invented answer.",
  "rubric": "The acceptance criteria used for this judgment.",
  "feedback": "The specific error and corrective next step."
}
```

Allowed `mode` values are `diagnostic`, `practice`, `check`, `checkpoint`, and
`review`. Only `practice` is unscored for streak purposes. Outcomes and their
effects are defined in the assessment reference.

Record multi-objective exercises as separate judgments sharing a `task_id`.
Do not reuse a task ID for another scored judgment on the same weakness.
An interrupted task can first have a `not_attempted` record and later have one
submitted scored judgment. If a hint or solution was shown in between, the
resumed answer is not independent.

Retain attempted prompts and actual responses so task freshness, grading, and
independence can be audited. A record for an invalid question or judgment must
explain the correction in feedback. Replay dependent summaries after corrections.
Preserve the learner-facing prompt's Markdown and line breaks in saved text.
On resume, render that text normally; do not show JSON escapes or wrap the entire
prompt in a code fence. A display-only correction retains the same question and
task IDs and does not create a new diagnostic exposure or scored attempt.

```json
{
  "id": "weakness-reversed-conditioning",
  "objective_id": "objective-conditional-probability",
  "description": "Interchanges P(A|B) and P(B|A).",
  "required_evidence_types": ["explain", "apply"],
  "success_streak": 0,
  "status": "active"
}
```

Allowed weakness statuses are `active`, `mitigated`, and `retention_confirmed`.
Derive them from attempts, not the date. Historical attempts preserve previous
mitigation and retention achievements after a gap is reopened.

When registering a new weakness, link the triggering judgment to it. Do not
reinterpret earlier untargeted successes as three independent checks of the
newly identified gap.

## Review queue

Entries should identify an objective, an optional weakness, a reason, a priority,
an optional `suggested_after` timestamp, and the last relevant evidence.
Priorities are ordinal recommendations, not precise forgetting probabilities.

Select from:

- Prerequisites needed for today's task.
- Previously fragile or repeatedly reopened gaps.
- Concepts not checked for a relatively long time.
- Previously mitigated concepts needing delayed evidence.
- A small sample of apparently strong material to detect hidden gaps.

Do not bulk-populate a debt queue for every missed day. A suggested review date
is not a deadline. Update priorities when the learner returns.

## Resume position

Preserve:

- The stage and current phase/objective.
- The exact unfinished prompt, task ID, submitted partial work, and whether
  hints, solutions, or resources were shown.
- The next useful action and any unresolved learner question.
- A pending follow-up choice, the choices offered, and the concept being discussed.
  Keep this separate from a scored problem; asking for clarification before
  practice is not an attempt or a solution hint.
- The mental model already introduced, any diagram or analogy used, and its limits.
- Important notation, assumptions, and software versions.

Set `pending_task` to null when no task is open. Do not grade an unfinished task
as a failure. A resumed task is not fresh solely because the session changed.
Set `pending_choice` to null when no interaction choice is awaiting a response.
After a pause at the follow-up invitation, resume that choice rather than silently
launching a new problem.

If session metadata is incomplete after an abrupt disconnect, preserve the
unknown end time. Use available timestamps to orient the learner, but do not
invent a precise absence length.

## Return-and-resume procedure

1. Load and validate the checkpoint where possible.
2. Orient the learner in one sentence and establish today's time budget.
3. Resume any pending follow-up choice or unanswered question first. Otherwise
   resume an open capstone from its saved materials without a solution-priming
   recap or a new task ID. If neither applies, offer one to three targeted probes,
   adjusted to time and uncertainty.
4. Probe before reteaching when the purpose is to assess retention.
5. Continue immediately if performance holds. Do not mandate a recap.
6. Repair specific demonstrated gaps when it does not.
7. If a check is declined, keep the old evidence and label current retention
   unverified; do not fabricate a pass or reset the streak.

After a long gap, use progressively deeper probes if initial checks reveal
prerequisite trouble. Do not restart the entire course automatically. After a
short gap, a fragile dependency can still deserve review.

## Session wrap-up and roadmap context

Save a short `summary` with each session: what was introduced or explored, what
was practiced, what was independently demonstrated, remaining gaps/questions,
and the next action. Link to concept/objective and attempt IDs where available.
Preserve partial learning even when the learner stops before a scored task.
Use `summary.covered_concept_ids` for concepts introduced or worked on, and link
independently demonstrated objectives to their attempt evidence. Count the union
of covered IDs across sessions, not repeated appearances of the same concept.

Derive roadmap counts from the agreed concept inventory and current evidence:

- The denominator is unique in-scope required concepts; report optional and
  explicitly deferred concepts separately.
- "Covered" means introduced or worked on, not mastered.
- "Independently demonstrated" requires evidence for all required linked
  objectives at the agreed depth, with relevant weaknesses mitigated and applicable
  gates met. Do not infer this from a selected option or a completed explanation.
- Count completed phases separately from the index of the current phase.
- Reopened gaps may change current demonstrated counts without erasing historical
  achievements. Saved counts are dated snapshots, not a second source of truth.

Example: "Today we explored one new concept and practiced two older ones.
Roadmap: 3/6 required concepts covered, 2/6 independently demonstrated; 1/3 phases
complete, working on phase 2. Next: practice the remaining distinction."

If totals are provisional or unavailable, say so and describe the actual
placement/planning progress instead. Do not invent counts or compare totals
across a scope change without explaining it. Keep the progress sheet and the
learner-facing wrap-up consistent with the structured evidence.

## Optional validation

`scripts/validate_state.py` reads a checkpoint without modifying it. It checks
core references, adaptive placement budgets and exposure records, and weakness
streaks and retention flags. It is not a JSON Schema engine and does not
exhaustively validate every optional record.

It cannot judge scientific correctness, semantic task novelty, whether a delay
was meaningful, whether a round genuinely adds difficulty/breadth/depth, or whether
the learner actually worked independently. It can reject missing or duplicate
purpose text, but cannot prove that differently worded purposes are substantively
distinct. The tutor must keep evidence for those judgments.
Capstone selection, semantic coverage, rubric quality, and optional metadata are
not automatically validated; check them against the capstone reference and
conversation scenarios. Capstone attempts still receive the core bookkeeping checks.
