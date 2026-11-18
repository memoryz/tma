# Assessment and mastery policy

Read this before placement, grading, or phase progression.

## Define evidence before asking

For each objective, specify the capability, prerequisites, required or optional
status, and a rubric. For each scored task, prepare a valid reference solution
or acceptance criteria before judging the learner.

Track breadth as coverage of concepts and relationships. Track depth through
demonstrated capabilities such as recall, explanation, application, prediction,
derivation, diagnosis, and transfer. They are evidence types, not a universal
ladder that every topic must follow.

Examples:

| Objective | Useful evidence |
| --- | --- |
| Understand a database index | Explain its mechanism; choose an index for an unfamiliar workload and justify tradeoffs. |
| Understand a derivative | Explain rate of change; compute one; interpret units and assumptions in a new setting. |
| Understand Bayes' rule | Derive it from conditional probability; apply it to a new base-rate problem. |

A purely factual objective can legitimately require recall. A conceptual
objective normally requires more than recall alone.

## Option-first surveys

For intake, goals, background, confidence, and pacing preferences, offer a small
set of concrete choices, with "Other" or "Not sure" where appropriate. Allow
multiple choices when the question calls for them and accept the learner's own
wording. Do not force them to invent a learning plan from a blank prompt.

Example: "What would be most useful: a broad overview, understanding why it works,
solving problems or building something, or help choosing a direction?"

These are unscored surveys. Save their answers with the goal or relevant
preference; do not create mastery attempts or weaknesses from self-ratings.

## Question presentation

Render the learner-facing problem and options as Markdown, not literal Markdown
source inside a plain-text form or a code block enclosing the whole question.
Use headings and lists to separate context, evidence, and the task. Fence actual
code or log excerpts individually, with an appropriate language label.
Keep equations readable using notation the host supports.

When a required response dialog cannot render Markdown, display the rich context
and options in the normal conversation, then collect the answer through a short
plain-text dialog. Its field labels and choices must contain no formatting-only
Markdown markers. Preserve stable option IDs and the same option meaning in both
places. Do not shorten away distinctions needed to answer the question.

Keep the answer key and rubric separate. Splitting presentation and response
collection does not create another question, assessment exposure, or scored
attempt. Wait for the learner's actual answer and preserve the existing budget
and independence rules.

## Adaptive placement

The goal is an actionable map of existing knowledge and gaps, not completing a
questionnaire or finding an arbitrary failure score.

### Limits and coverage

- At most five rounds, each containing one to four presented questions.
- At most twenty presented knowledge-assessment questions across all rounds
  and sessions combined. Either limit may be lowered for the learner.
- No minimum number of questions or rounds. Early stopping is desirable once
  more questions would not materially change the learning route.

Map essential prerequisites and major branches in the agreed scope first.
Prepare a small initial round and a coverage blueprint, not a fixed sequence of
twenty questions. Reserve capacity for both breadth and clarification; do not
spend the full budget escalating difficulty in the first branch sampled.

Round 1 establishes an easy, broad baseline relative to the learner's background.
Every later round must explicitly progress in at least one of these dimensions:

| Progression | Unique information sought |
| --- | --- |
| Harder | Can the learner handle greater difficulty where foundations already hold? |
| Wider | Does understanding extend to an important branch or prerequisite not yet sampled? |
| Deeper | Can the learner explain a mechanism, justify an assumption, transfer an idea, or resolve a specific ambiguity? |

These are not mandatory separate stages. A round can advance more than one
dimension. A simpler prerequisite check can resolve a new causal uncertainty
inside a deeper round, but does not justify a whole repetitive or regressive
round. Do not infantilize an experienced professional.

Before each question, identify its distinct diagnostic purpose: what competing
explanations it distinguishes and how the response could change the starting
phase or planned instruction. Changing numbers or wording without changing
that inference is redundant. A confirmation question is useful only when it
resolves a specific remaining ambiguity, not when it repeats an established gap.

### Decisions after answers and rounds

For each sampled branch, retain the strongest independent evidence, the next
untested depth, confirmed or tentative gaps, and the basis for uncertainty.
Use ordinary qualitative judgments, not invented psychometric probabilities.

- A clear foundational misconception or explicit lack of prerequisite knowledge
  can be enough to locate a starting point for that branch.
- An ambiguous error, unfamiliar notation, or lucky-looking choice may justify
  one discriminating follow-up, if budget remains. Do not diagnose from a typo.
- Strong answers justify a harder probe where its result could change placement.
  Multiple-choice recognition alone does not establish a deep knowledge floor.
- Once a branch's boundary is clear enough, stop probing it. Sample another
  important unknown branch if that information could change the roadmap.
- Stop the entire assessment when essential prerequisites and priority branches
  are sufficiently mapped for the agreed starting scope, or when a cap or the
  learner's request requires stopping. Do not stop globally just because one
  isolated gap appeared while important branches remain unknown.

Sufficient coverage does not mean checking every branch. A decisive prerequisite
gap may already determine the starting route; stop globally if additional probes
would not change it, and explicitly preserve the unsampled branches as unknown.

After each round, give a short plain-language update: what is established,
what is still uncertain, and how the next round would be harder, wider, or
deeper. Offer to continue, pause, or start learning from the provisional profile;
respect today's time. If no distinct next question could change the plan, stop.
Do not force all five rounds or repeat a settled misconception.

At the end, report per-branch strengths, depth boundaries, gaps with evidence,
and unsampled/uncertain areas. State the stop reason and recommended starting
phase. The three-success rule is for mitigating learning gaps, not a requirement
to keep testing them during placement.

### Question accounting

One question is one independently answerable diagnostic prompt. Choosing an
option and briefly explaining the same claim may be one question. Independent
subparts count as separate questions with separate IDs, even if sent together.
Every separately requested reasoning follow-up, confirmation, easier
prerequisite probe, or replacement for a flawed prompt also consumes a question.
Invalid or unanswered presented prompts still consumed the learner's attention
and remain in the budget; they are not automatically scored as failures.

Record a question when first presented, not only after an answer arrives.
Repeating an unfinished question after interruption uses its original ID and
does not spend budget again. A new task or newly requested diagnostic demand
needs a new ID. Multiple objective judgments of one question are not multiple
question exposures, and must not hide independent subquestions.

Intake preferences, administrative check-ins, and learner-initiated clarification
that does not test new knowledge do not count. Normal teaching and later mastery
practice are separate, but do not relabel an ongoing placement survey to get
around either cap.

Before every question, check the cumulative question count and current round
capacity. At four questions, finish that round before opening another. Never open
a sixth round or present a twenty-first question. Pause/resume and session gaps
do not reset counters.

### Options and deeper evidence

Start survey-style placement questions with a few plausible options and a
"Not sure yet" choice. Use distractors that distinguish actual misconceptions,
not trick wording. Keep the answer key separate.

Follow up with a short explanation, prediction, derivation, or solution when
assessing depth. A selected option is a low-friction screen, not proof that the
learner can explain or apply the idea. Record choice-only responses with the
diagnostic question as screening evidence, not as qualifying scored successes
in the weakness ledger. Preserve selected option IDs and the actual response.
Do not treat an omitted optional explanation as a scored failure.

Use productive short answers and independent problems for deeper evidence and
mastery checks; not every practice task should become multiple choice. A combined
choice-and-reason response can qualify only if the independent reasoning meets
the full rubric. Some challenging questions should expose the current boundary
of understanding, not manufacture a failing score.

Do not reveal an answer key alongside its questions. If feedback or a hint teaches
a concept during placement, label later evidence appropriately. Do not describe
post-instruction improvement as prior knowledge.

## Grade the intended capability

Use these outcomes:

- `pass`: meets the task's rubric.
- `partial`: meaningful correct work but an essential criterion is unmet.
- `fail`: submitted answer does not demonstrate the capability, including an
  explicit "I don't know."
- `not_attempted`: no submitted answer, including an interrupted task.
- `invalid`: flawed or ambiguous task, exposed answer, or voided grading.

Track independence separately. A correct answer produced with a solution hint is
`pass` with `independent: false`, not independent mastery. Permitted tools must
be defined by the task: documentation can be legitimate in an engineering task,
whereas a closed-note retrieval question excludes it.

Ask for clarification before interpreting an ambiguous response as a conceptual
error. Give appropriate credit for alternative methods and mathematically
equivalent expressions. Check domains, assumptions, units, boundary cases,
and numerical or software results where relevant.

When feedback is challenged, recheck the solution. Preserve the original response;
mark an erroneous judgment invalid with a correction note rather than penalizing
the learner. Review any dependent mastery claims after a correction.

## Explain and repair a gap

Use plain language before specialist terminology. Say what the learner's current
model predicts, identify the missing distinction, and rebuild the relevant
part of the model with a concrete example. Define a new term before relying on
it in another explanation; add formal detail without sacrificing accuracy.

Where applicable, show a counterfactual:

1. If the mistaken assumption were true, what would we expect?
2. What actually happens, or what follows from the correct assumptions?
3. Why does that difference change a prediction, solution, or decision?

For example: "If 'independent' meant 'cannot happen together,' two separate fair
coin tosses could never both land heads. They can. Here, independent means
knowing one result does not change the chance of the other."

Make thought experiments explicit and state an analogy's limits. Use a diagram
if it clarifies the relationship, and describe its meaning in words. Do not add a
counterfactual merely to follow a formula when a direct explanation is clearer.

Before the next practice scenario, invite a follow-up, another representation,
practice, or a pause, and wait unless the learner has already requested the next
scenario or continuous practice. A follow-up during teaching is not a scored
attempt and does not alter a weakness streak. If a solution hint is requested
during an already-open scored task, the existing independence rules still apply.

## What a weakness means

Create one weakness per specific gap tied to one objective, supported by an
observed response. A hypothesized root cause stays provisional until checked.

Good: "Treats P(A|B) as interchangeable with P(B|A)."
Poor: "Bad at probability."

For a multi-part exercise, grade objectives separately. A mistake on one part
must not reset an unrelated weakness. One exercise can produce multiple judgment
records, but at most one qualifying judgment per weakness.

## Exact three-success rule

Each weakness declares `required_evidence_types`. For a conceptual gap, a useful
default is `["explain", "apply"]`; select types appropriate to the objective.
A narrow factual gap may use only `["recall"]`.

A scored check is eligible only when it uses a fresh task and explicitly assesses
the objective. Placement, independent checks, phase checkpoints, and reviews may
be scored. Guided practice is not scored for mastery.

For each weakness, replay its recorded attempts in chronological order:

| Event | Effect |
| --- | --- |
| Independent `pass` on a fresh scored task | Append the success; retain the latest three successes in the current run. |
| Scored `partial`, `fail`, or hint-assisted answer | Clear the success run and reopen the gap. |
| Guided practice, even with mistakes | No change to the scored success run. |
| `not_attempted` or `invalid` | No change. |
| Unrelated objective or weakness | No change. |
| Time passing or a new session starting | No change. |

The streak is the length of the current run, capped at three.
A weakness is `mitigated` when the run contains three successes and those
successes collectively cover its required evidence types. A streak of three
without the required variety remains `active`; ask a suitable fresh task.
While establishing mitigation, evaluate the latest three successes. Once earned,
mitigation remains until a scored non-independent or unsuccessful answer; later
correct answers do not revoke it merely because their evidence types differ.

"Consecutive" refers to scored attempts for that weakness, not adjacent
conversation turns or consecutive days. Do not triple-count several parts of
one task or repeated attempts at the same solution.

Freshness is substantive: change the reasoning demand or relevant context,
not merely variable names or sentence wording. Do not count immediate reproduction
of a demonstrated solution. Guided retries stay practice; use a different task
for the next scored check.

## Retention and reopening

After mitigation, an independent successful retention review can change the
status to `retention_confirmed`. It must be in a later session, after a meaningful
delay, without first showing the explanation or solution. Record why it counts
as delayed evidence in `retention_basis`. A session reopened moments later is
not automatically a retention test.

The check that first establishes mitigation cannot also establish retention.
Repeated later reviews strengthen evidence; no number guarantees permanent
understanding. Retention status describes observed checks, not a lifetime claim.

A subsequent scored failure, partial answer, or hint-assisted answer resets
the streak and returns the status to `active`. Preserve older achievements in
the attempt history. Rebuild the three-success run with new tasks.

Without a new check, retain the previous status and show when it was last tested.
"Not checked recently" and "demonstrated a gap" are different facts.

## Phase gates

Move on when:

1. Each required objective has independent evidence at the agreed depth.
2. Weaknesses relevant to required outcomes are mitigated or retention-confirmed.
3. No unresolved prerequisite blocks the next phase.
4. A fresh integrative task meets its rubric, unless the phase is genuinely too
   narrow for integration; in that case use an appropriate independent exit task.

Optional enrichment does not block the gate. A missing future retention review
does not block it either. An average score cannot compensate for a missing
essential capability.

If a later failure affects a prerequisite, repair that dependency before relying
on it again. Keep the historical phase result and mark its current status
`needs_repair` where appropriate; do not erase completed work.

The learner can request an early move, skip assessment, or change goals.
Explain the tradeoff briefly, record the bypass or revised scope, and do not
relabel unmet outcomes as mastered.

## Final capstone

After the agreed phases, use the interview-capstone reference to build one
realistic, open-ended transfer scenario around at least three eligible learned
gaps when available, or all one or two if fewer exist. With no eligible learned
gaps, assess core learned objectives without inventing weaknesses.

Prepare a per-target rubric and assess the targets separately. Record checkpoint
judgments with a shared scenario task ID, at most once per weakness. Interview
subparts, turns, and continuations cannot supply a three-success streak by
themselves. Unelicited targets remain untested; solution assistance affects the
relevant target's independence, not automatically every target.

The overall case and every selected target must meet the rubric independently
for an independent pass. Repair only affected gaps and use fresh retests.
Completion alone does not establish delayed retention or erase unmet phase gates.
