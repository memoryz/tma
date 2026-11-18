# Conversation acceptance scenarios

These are manual trials for an assistant running the skill, not claims that
tutoring quality has been empirically validated. Use synthetic learner answers
or a consenting tester's responses. Do not publish identifiable learning records.

The Python tests check bookkeeping and package integrity, not teaching quality.
For each trial, record the host/model, date, topic, prompt sequence, observed
behavior, and pass/fail evidence.

## 1. Technical topic, breadth followed by depth

Start: "Teach me database indexes. I build services but do not understand query
plans. I have 15 minutes today."

Expected:

- Establishes practical goals and proposes a separate progress workspace.
- Researches suitable official or authoritative sources and notes relevant versions.
- Produces a prerequisite map and a small easy/broad initial round, then selects
  later questions adaptively rather than dumping twenty questions.
- Offers a few clear survey choices while accepting free-form responses.
- Uses answers to distinguish conceptual understanding from terminology.
- Offers breadth, depth, or mixed direction after placement.
- Defines observable phase goals and exit rubrics.

## 2. Mathematical topic and equivalent answers

Start: "Teach me derivatives deeply enough to understand gradient descent."

During practice, submit a mathematically correct alternative derivation or an
equivalent algebraic form. Later, make a genuine domain or chain-rule error.

Expected: accepts the valid method, verifies the reasoning and assumptions,
and creates a precise gap only for the actual error. Does not equate unfamiliar
notation or one arithmetic slip with a broad conceptual failure.

## 3. Five-minute session and interrupted placement

Start: "Teach me Bayesian inference. I only have five minutes."
Leave during placement. Return later with another short budget.

Expected: reduces the immediate workload, saves partial placement, marks
unsampled coverage unknown, and resumes without inventing answers or restarting
the entire assessment. Preserves the same round and cumulative question budget.
Today's session can accomplish just one useful task.

## 4. Irregular gap does not reset a streak

Begin with a synthetic weakness at two independent successes. Return after a
gap of several months.

Expected: preserves the 2/3 streak, orients briefly, and offers a targeted check.
A fresh independent success with the required evidence variety reaches 3/3.
The gap alone does not reset progress or establish retention confirmation.

## 5. Long-gap retention holds

Begin with a previously mitigated weakness. Return months later and answer
a fresh, independent pre-recap review correctly.

Expected: no compulsory course restart, no overdue lecture, and no needless
reteaching. Records delayed evidence, including its basis and date.

## 6. Retention fails selectively

Return to a completed phase. Answer one prerequisite check incorrectly while
answering another correctly.

Expected: reopens only the demonstrated gap, preserves historical achievements,
and repairs affected dependencies. Does not reset unrelated streaks or label the
entire phase permanently forgotten.

## 7. Hints, retries, and three successes

Give two independent correct checks, then request a solution hint on the next
scored check. Correctly finish it. Complete three fresh independent checks later.

Expected: the hint-assisted scored answer resets the streak; the same-task retry
is not fresh. Guided practice errors do not reset later scored successes.
Mitigation requires three consecutive independent passes and required evidence
variety, not three identical recalls of the tutor's explanation.

## 8. Abrupt interruption mid-problem

Stop after seeing a hint and writing part of a solution. Resume the next session.

Expected: restores the prompt, partial work, and shown hint. Does not count the
interruption as failure or the resumed solution as an independent fresh success.

## 9. Phase gate and learner agency

Pass most questions but miss an essential prerequisite. Ask to advance anyway.

Expected: explains the specific unmet gate, offers focused repair, and records
an explicit bypass if the learner still proceeds. Does not claim mastery or
allow a high average to conceal the gap. A pending delayed review alone does
not block advancement.

## 10. Challenged grading

Give a valid but unexpected solution and challenge an incorrect tutor judgment.

Expected: rechecks rather than defending its first answer, corrects the judgment,
preserves the original response, and replays streaks without penalizing the
learner for a tutor error.

## 11. No file or web tools

Run in a host without file persistence or browsing.

Expected: does not invent freshly verified citations or saved files. Uses a
clearly labeled conversation-only workflow, provides an exportable checkpoint,
and identifies source uncertainty when relevant.

## 12. Declined review and changed goal

Return after a gap, decline re-entry checks, and change from derivation-heavy
depth to a broad conceptual overview.

Expected: respects the choice, records retention as unverified, revises required
outcomes transparently, and defers removed material without calling it mastered.

## 13. Choice-based surveys without recognition-only mastery

Start: "I want to learn probability, but I don't know what goal to choose."
Select offered goals and background choices. For placement, select correct
options without supplying the optional reasoning.

Expected: offers a few concrete options, including uncertainty or another
direction where appropriate, rather than only "What do you want to learn?"
Records choices and distinguishes screening from independent explanation or
application. Does not grant three-success mitigation for three selected letters,
or score an omitted optional explanation as a failure. Offers short productive
follow-ups when deeper evidence is needed.

## 14. Plain language for an unfamiliar idea or gap

Say: "I don't know what backpressure means. That explanation used several other
terms I don't know either."

Expected: rebuilds the explanation in everyday language with a familiar example,
defines necessary terms before relying on them, and preserves technical accuracy.
Does not respond with another unexplained stack of jargon or assume professional
experience means subject familiarity. Adds formal detail when useful or requested.

## 15. Mental model and diagram before scenarios

Start a new teaching segment on request queues or function composition. Say:
"Can you show me how the pieces connect?"

Expected: identifies the parts and relationships before launching a practice
scenario, uses a small labeled diagram where helpful, and explains it in words.
States an analogy's limits. Does not assign a fixed visual learning style or
rebuild the same model unnecessarily before every later scenario. Does not
reveal solutions before a purported untaught placement or retention probe.

## 16. Follow-up opportunity and interrupted check-in

After an explanation, choose "Ask a follow-up" instead of practice. Ask about a
missing connection, then pause before choosing whether to try the next scenario.
Return in another session. Later, explicitly request continuous practice.

Expected: offers a follow-up/another explanation/practice/pause choice and waits
without appending the new problem. Answers the actual question, saves the pending
choice, and resumes it after the pause. The conversation is not a failed attempt
or a hint-assisted scored answer. Honors continuous-practice preference without
redundant prompts; hints during an already-open scored task still affect independence.

## 17. Session wrap-up in roadmap context

Use an agreed roadmap of six required concepts in three phases, plus one optional
concept. Two required concepts are independently demonstrated and phase 1 is
complete. Introduce a third required concept with guided practice only in phase 2,
then end the session.

Expected: summarizes what was explored, practiced, and independently demonstrated
in plain language. Reports 3/6 required concepts covered, 2/6 independently
demonstrated, 1/3 phases complete, and phase 2 as current. Does not count the
optional concept in the required total or call the guided concept mastered.
Saves a dated session summary and one next action. With no established inventory,
reports totals as unknown/provisional instead of inventing a denominator.

## 18. Counterfactual makes a gap's importance concrete

During probability teaching, confuse independent events with events that cannot
happen together. Ask: "Why does that distinction matter?"

Expected: explains the distinction in plain language and, where useful, contrasts
what would follow if the mistaken assumption were true with what actually happens.
For example, separate coin tosses can both land heads. Connects the difference
to a prediction or decision and then repairs the model. Does not present a
thought experiment as an observed fact or force a counterfactual when a direct
explanation is clearer.

## 19. Each round progresses harder, wider, or deeper

Use an initial easy round across prerequisites and major branches. Demonstrate
strong vocabulary in one branch, uncertain reasoning in another, and no evidence
yet for a third important branch.

Expected: explains how a later round adds difficulty, breadth, or depth based
on the actual responses. It may raise challenge, test the unsampled branch,
or resolve the reasoning uncertainty. Each question has a distinct purpose
and a plausible effect on placement. Does not repeat the baseline under a new
round number or assume that a "deeper" label proves genuine progression.

## 20. Early stopping is normal, not a failed questionnaire

In one trial, reveal a decisive missing prerequisite within the first few
questions. In another narrowly scoped trial, demonstrate the target capability
independently without errors.

Expected: stops once the starting route is clear, whether the profile is weak
or strong. Does not force five rounds, twenty questions, a minimum of ten
questions, or an eventual failure. Records the evidence, stop reason, and
unknown branches. The three-success remediation policy does not prolong placement.

## 21. A local gap does not erase the need for useful breadth

Answer a question in one branch incorrectly while several other branches could
still materially change the starting roadmap.

Expected: stops redundant probing of the established local gap but uses a wider
round when that would improve the plan. Does not declare the whole topic known
or unknown from one error. Reports independent depth, confirmed/tentative gaps,
and unsampled areas separately.

## 22. Hard caps include follow-ups and survive interruptions

Approach twenty presented questions across five rounds, including separately
asked reasoning follow-ups, an invalid prompt, and a question left unanswered
before a session break. Resume afterward.

Expected: invalid and unanswered exposures remain in the count. Resuming the same
unfinished question preserves its ID, round, and budget. Never asks a twenty-first
diagnostic question, hides extra independent subparts, or relabels more survey
questions as practice. A separate trial with five short rounds also stops before
a sixth round, even if fewer than twenty questions were asked.

## 23. Unique diagnostic purpose, not cosmetic variation

After a misconception is clear, propose another question that only changes
numbers. Separately, provide an ambiguous answer that could reflect either
a notation issue or the misconception.

Expected: skips the redundant question. In the ambiguous case, may spend one
question on a contrast that distinguishes those specific explanations. Saves
the distinct purpose and how the response changes placement. Does not ask
repeated confirmations merely to fill the remaining budget.

## 24. Legacy placement does not grant a fresh allowance

Resume an older checkpoint with twelve questions already asked but no reliable
round log.

Expected: preserves historical counters and evidence. Reconstructs rounds only
where reliable history supports it; otherwise ends with a provisional profile
rather than inventing round history or granting five more rounds. Does not modify
the learner's actual records just because the skill's template changed.

## 25. Technology capstone genuinely integrates learned gaps

Use synthetic history with four eligible mitigated gaps from past sessions,
including retry amplification, timeouts not proving an operation had no effect,
and duplicate side effects without idempotency. Finish the agreed service-
reliability roadmap and ask for the final scenario.

Expected: selects at least three distinct learned gaps and explains the private
target-to-evidence mapping. Creates one realistic design or incident-investigation
case whose decisions require those distinctions. Uses consistent synthetic logs
or constraints, not three unrelated exercises. Presents an open-ended brief
without the solution map; lets the learner frame the problem and ask clarifying
questions. Does not provide a fresh mental-model walkthrough before assessment.

## 26. Scientific investigation, not just formula substitution

Finish a measurement-science roadmap with historical learned gaps about
calibration bias, confounding, and measurement uncertainty. Ask: "What would a
science capstone look like? I don't want just another calculation."

Expected: offers a realistic observation/data investigation, such as instruments
disagreeing under changing conditions. Requires competing explanations, evidence,
predictions, a discriminating measurement or experiment, and limits on the
conclusion, at the agreed depth. Each selected gap is necessary to the case.
Accepts defensible alternatives and does not invent a unique cause when data are
ambiguous. Does not require untaught experimental methods or domain knowledge.

## 27. Mathematical modeling with assumptions and validation

Finish a calculus roadmap with prior learned gaps about setting up rates,
tracking units, and respecting domain constraints. Request a final interview case.

Expected: poses an appropriately scoped modeling problem, such as reasoning about
a finite-capacity tank with changing flows. Requires assumptions, a justified
method, derivation, interpretation, and checks, not just naming the right formula.
Accepts equivalent valid approaches. Selects only previously learned gaps and
does not add untaught machinery to make the scenario appear sophisticated.

## 28. Fewer than three gaps and early formative attempts

Run separate histories with two, one, and zero eligible learned gaps. Also try
an early interview with unresolved required prerequisites.

Expected: targets all two or one, respectively. With no eligible gaps, uses
learned core objectives and explicitly records the absence of eligible targets.
Never fabricates history or splits one gap into aliases to reach three. Existing
active gaps remain visible. Offers repair first or records an explicitly formative
early attempt and unmet gates; does not use a zero-eligible fallback to claim the
learner has no gaps or has completed all required learning.

## 29. Per-gap independence and no triple-counted successes

In a three-target capstone, ask for a units clarification and later request a
solution hint on one target. Independently solve the other two. Submit several
subparts across interview turns.

Expected: units clarification is not automatically a hint. Actual solution
assistance affects the relevant target. Saves at most one scored checkpoint
judgment per weakness on the shared task ID. Reopens the hinted gap under the
existing policy while preserving the other gaps' achievements. Does not award
three successes for three subparts, average away the missing independent target,
or automatically mark checkpoint success as delayed retention confirmation.

## 30. Paused capstone resumes the same interview

Before starting, ask a follow-up and then choose a short interview session.
Pause partway through and return after an irregular gap.

Expected: honors the pre-start follow-up opportunity without launching the case
prematurely. Restores the exact brief, supplied evidence, pending question, partial
reasoning, permitted tools, and assistance. Resumes the same task ID without an
automatic failure, new success, or solution-priming re-entry lesson. The completed
interview is assessed once per target. The wrap-up explains what was integrated,
what remains fragile, and the result's place in the whole roadmap.

## 31. Untested target and focused repair

Produce a polished capstone answer that avoids one selected target. In a separate
run, make an error in one gap while showing sound integration elsewhere. Ask to
defer the remaining work.

Expected: a missing target stays untested rather than receiving an invented pass
or failure. Uses a neutral follow-up if it can elicit the missing evidence.
Repairs and freshly retests the actual error, preserving unrelated progress;
does not count the same solved case again. Repeats full integration only if that
capability remains unproven. Records paused/deferred or needs_repair truthfully
rather than claiming the final integration check passed.

## 32. Rich prompts render as Markdown

Request a database-index question containing SQL, a short incident scenario with
logs, and a mathematics problem with notation. Inspect both newly presented
questions and one resumed prompt.

Expected: headings, emphasis, lists, and inline code render in the conversation.
Only the SQL, logs, or other genuinely monospaced content use individual code
fences; the entire prompt is not a literal code block. Mathematical notation is
readable without unsupported raw LaTeX delimiters. No JSON escapes, quoted string
dumps, or unnecessary escaped Markdown appear. Answer keys stay separate.
Resuming or correcting only the display preserves the same question/task IDs,
diagnostic exposure count, and mastery evidence.

## 33. Plain-text choice dialogs collect answers, not Markdown source

Use a host whose required question dialog displays Markdown markers literally.
Present a survey or diagnostic question with formatted context and options.

Expected: rich context and options are presented through the Markdown conversation
surface, while the required dialog contains only a short plain-text response
request and unformatted labels. Option IDs and meanings match in both places;
the learner does not have to read raw formatting syntax to answer. The tutor
still uses the required question tool, waits for the response, and counts the
combined presentation once, not as two diagnostic questions. If no host surface
renders Markdown, uses a readable plain-text fallback without claiming to have
fixed the host renderer.

## Trial record

| Field | Observation |
| --- | --- |
| Host/model and date | |
| Topic and scenario | |
| Time budget and session gaps | |
| Expected behavior observed | |
| Unexpected behavior and exact evidence | |
| Pass / fail / inconclusive | |
| Anonymized checkpoint location | |
