# Final interview-style capstone

Use this after the agreed learning phases to assess whether the learner can
combine what they learned in a realistic, unfamiliar situation. This is one
coherent case, not a summary lecture or three unrelated quiz questions.

## 1. Select the learned gaps

Read the historical weakness log, objective evidence, roadmap, and session notes.
An eligible target is a real, in-scope gap that was identified, taught, and
mitigated or retention-confirmed before capstone selection. Normally repair
active blocking gaps before starting the final independent check.
An early formative interview is allowed if the learner prefers, but record the
unmet phase gates and coaching. Do not present it as completed independent
learning while those gates remain unmet.

- If three or more eligible distinct gaps exist, select at least three.
- If only one or two exist, target all of them.
- If none exist, target suitable learned core objectives and record that this
  is an objective-based capstone, not invented gap coverage.

No eligible learned gaps does not mean no historical gaps: retain any active
gaps and unmet phase gates. Do not use the objective-based fallback to hide them.

Prioritize consequential, recurrent, interconnected gaps. Draw from different
past sessions when available, but never invent a multi-session history.
Do not split one misconception into several names to satisfy the count.
Use a manageable selection rather than every historical weakness. The selected
gaps must genuinely interact in one scenario; linked stages of one case are
acceptable when needed.

Save each target ID, its evidence and status at selection, and why it matters.
Keep this snapshot after the capstone even if a gap is subsequently reopened.
One successful final task does not repair an active weakness's missing
three-success run by itself.

## 2. Choose a realistic format

| Domain | Open-ended case | Evidence to elicit |
| --- | --- | --- |
| Software or systems | Design a service under workload and reliability constraints. | Requirements, architecture, tradeoffs, failure behavior, and validation. |
| Operations | Investigate a simulated live incident from event logs, metrics, and a deployment timeline. | Hypotheses, evidence correlation, missing observations, corrective plan, and verification. |
| Science | Explain conflicting observations or an anomaly using supplied measurements. | Competing mechanisms, predictions, assumptions, uncertainty, and a discriminating test. |
| Science | Defend a measurement or experiment plan under practical constraints. | Variables, controls, confounders, expected outcomes, and what would falsify the explanation. |
| Mathematics | Build and defend a model for a real decision or phenomenon. | Assumptions, choice of method, derivation, domain constraints, and checks of the result. |

These are formats, not mandatory new topics. Match the learner's actual scope and
depth; do not require systems expertise from someone learning elementary algebra.
For science, solving a problem can work, but interpreting evidence and designing
a decisive test often provide a richer integration task than formula substitution.

For example, a measurement-science learner could investigate why two instruments
disagree as room temperature changes. An appropriate case might integrate prior
gaps about calibration bias, confounding, and measurement uncertainty. Supply a
small dataset and ask for an explanation and a test that would distinguish it
from alternatives. Use those targets only if they were actually learned.

Use synthetic or exercise-provided logs and data, clearly labeled. Check that
timestamps, units, relationships, and numerical examples are internally
consistent. Provide enough information for reasonable progress. Deliberate
ambiguity is acceptable only if identifying missing evidence is part of the task.
Do not require actual production changes or access to a real incident.

## 3. Design backward from the targets

For each selected gap, privately map:

1. The specific earlier misunderstanding and evidence it was learned.
2. The scenario decision or reasoning step that requires the corrected model.
3. Observable evidence that would satisfy the objective at the agreed depth.
4. Likely errors, legitimate alternative approaches, and what would remain untested.

Ask whether someone could complete the case while avoiding a selected target.
If so, redesign that part: incidental vocabulary does not establish coverage.
Do not turn the prompt into an ordered recipe naming each technique to apply.

Use the learner-facing brief for context, constraints, supplied evidence,
permitted tools, and an open invitation to investigate or propose a solution.
Keep the target map, indicative reasoning, and scoring criteria in the separate
assessor record. Make the intended depth and broad success expectations clear,
without leaking a particular solution.

## 4. Interview rather than lecture

Before starting, offer the usual follow-up/practice/pause choice and agree on
today's time. The capstone prompt itself is open-ended, not multiple choice.
Let the learner organize their reasoning before directing attention to a target.

Follow their approach with a small number of useful neutral probes, one at a time:

- "What assumptions are you making?"
- "Which observation would distinguish those explanations?"
- "How would you check whether your proposal worked?"
- "What would change your conclusion?"

These are examples, not a required checklist or a turn-count target. Ask only
when a probe adds distinct evidence. Accept valid alternative solutions.

Clarifying requirements, units, or supplied log fields is normal interview
behavior, not a failure or automatically a hint. Naming the method to use or
revealing the missing causal link is assistance: record it for the affected
target rather than marking every target non-independent.

Do not rebuild the mental model or show a worked solution immediately before
this transfer assessment. If coaching is requested, provide it transparently,
record the assistance, and distinguish coached learning from an independent pass.
Do not invent contradictory facts to steer the learner toward a preferred answer.

## 5. Grade integration and preserve evidence

Judge the framing, reasoning, use of evidence, assumptions, tradeoffs where
relevant, and validation plan. Assess each selected gap explicitly; polished
language or a correct final number cannot conceal an essential misunderstanding.

Record one final judgment per assessed target, linking its objective and, when
applicable, its weakness. Objective-only targets use `weakness_id: null`.
Use a shared scenario `task_id`, `mode: "checkpoint"`, and the appropriate
evidence type, often `transfer`. At most one scored judgment may target the same
weakness on this task. Several interview turns or subparts do not yield several
successes. A target that was never elicited remains untested; do not fabricate
an attempt or a pass.

An independent capstone pass requires the overall rubric and every selected
target to be demonstrated independently. A scored partial, failure, or
hint-assisted answer follows the existing reopening rules for that gap only.
Preserve unaffected evidence and historical achievements. Support focused repair
and fresh retesting; repeat the full scenario only if integration itself remains
unproven. Do not reuse the solved case as a fresh independent success.

Capstone success is not automatically proof of long-term retention. The existing
retention-review policy still applies. Explain remaining uncertainty and offer
future review opportunities without imposing a fixed schedule.

## 6. Pause and debrief

The case can span sessions. Preserve the exact data packet, version of the brief,
pending interviewer question, partial reasoning, permitted resources, and any
hints. On return, resume the same case without counting the continuation as a
fresh task or injecting solution-priming review.

Debrief the integrated capabilities, each selected gap's evidence and current
status, any untested target, and one focused next step. Include the usual roadmap
context. A deferral or unfinished interview is not a failure, but it is not a
passed final integration check either.
