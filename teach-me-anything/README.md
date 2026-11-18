# Teach Me Anything

A portable Agent Skill for learning science, technology, engineering, and
mathematics through adaptive, evidence-based tutoring.

Designed for professionals with day jobs: sessions can be short, unpredictable,
and separated by days or months. The tutor adapts to what you can demonstrate
today, not a schedule you were supposed to follow.

## What it does

1. Researches the topic and maps prerequisites.
2. Assesses breadth and depth adaptively, capped at five rounds and twenty questions.
3. Helps you choose breadth, depth, or a mixture and agree on a phased roadmap.
4. Teaches through explanations, worked examples, practice, and targeted feedback.
5. Tracks specific weaknesses until three consecutive independent successes.
6. Uses checkpoints, cumulative practice, and opportunistic retention checks.
7. Ends with a realistic, open-ended interview capstone integrating learned gaps.

Surveys offer a few choices rather than a blank prompt. Teaching starts with a
plain-language mental model, with diagrams where useful, and offers room for
follow-up questions before a new practice scenario. Gap explanations use
counterfactuals when they clarify why a distinction matters. Session wrap-ups
connect what you learned today to your progress through the whole roadmap.
Placement starts with easy, broad probes. Each later round must become harder,
wider, or deeper, and each question must resolve a distinct uncertainty. It stops
as soon as the profile is useful enough to plan learning. Five rounds and twenty
questions are ceilings, not minimums or goals; follow-ups share the same budget
across sessions.

Learner-facing prompts use rendered Markdown, with code and logs fenced
separately rather than the whole question. If a response dialog displays plain
text, the formatted context stays in the conversation and the dialog collects
only the answer using short, unformatted labels.

Three successes establish initial mitigation under the chosen rubric, not a
guarantee of permanent understanding. The skill distinguishes mitigation,
retention evidence, and areas that have not been checked recently.

## Final capstone

The capstone targets at least three distinct, important gaps identified and
learned during the roadmap when available. With only one or two, it covers all
of them; with none, it assesses core learned objectives without inventing gaps.
The targets must be necessary to solving one coherent case, not three unrelated
questions or concepts merely mentioned in passing.

Examples include system design under constraints, troubleshooting an incident
from synthetic logs, explaining scientific observations and designing a test
between competing hypotheses, or building and validating a mathematical model.
For science, a routine calculation is only one possible format: evidence,
predictions, controls, confounders, and uncertainty can be the central challenge.
Use only concepts actually taught at the learner's agreed depth.

The tutor interviews rather than walks through a solution. It grades each target
separately, preserves the existing mastery rules, and supports pauses across
sessions. One case cannot supply three independent successes for the same gap.
The learner-facing brief and assessor criteria are separate until the debrief.

## Try it without installing

Ask your assistant to read [SKILL.md](SKILL.md) and follow its linked instructions.
For example, from the folder containing this package:

> Read `teach-me-anything\SKILL.md` and use it to teach me linear algebra.
> I use vectors at work but struggle with eigenvectors. I have 15 minutes today.

Other useful trials:

> Teach me how database indexes work. I want to understand query-plan tradeoffs.

> Teach me Bayesian inference, including enough mathematics to derive Bayes' rule.

> Resume my calculus topic from the saved progress folder. I have five minutes.

File access and persistence depend on the host. A conversation-only host can use
the workflow and export checkpoints, but cannot promise durable local storage.

## Install later

This package follows the [Agent Skills format](https://agentskills.io/specification).
Keep the complete `teach-me-anything` folder together: its references, templates,
and optional validator are part of the skill.

For Copilot CLI, run these commands from the directory **containing** the
`teach-me-anything` folder:

```powershell
copilot skill add .
copilot skill list
```

The first command registers a custom skills directory. Alternatively, copy the
complete skill folder into a skill location supported by your host.
Do not use a single-file install if it would omit the supporting files.
No installation or global configuration changes are required to inspect or test
this package.

## Progress belongs to the learner

The tutor proposes a separate topic-specific workspace, such as a folder under
`.learning` in the working directory. It does not populate this package with
personal learning records.

| File in a learning workspace | Purpose |
| --- | --- |
| `learner-state.json` | Authoritative evidence, sessions, streaks, review priorities, and resume position. |
| `roadmap.md` | Scope, source notes, concept map, phases, and exit criteria. |
| `progress.md` | Readable strengths, weaknesses, retention evidence, and next action. |
| `capstone-brief.md` | Final scenario, constraints, supplied evidence, and open-ended task, created when needed. |
| `capstone-assessment.md` | Separate target map, rubric, interview notes, and per-gap evidence, created when needed. |

Use separate workspaces for separate topics and learners. Do not publish real
learner records with the skill.

## Package contents

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main tutoring workflow. |
| [Learning science](references/learning-science.md) | Research basis and design limitations. |
| [Assessment and mastery](references/assessment-and-mastery.md) | Rubrics, evidence, and progression rules. |
| [State and resume contract](references/state-and-resume.md) | Portable records and irregular-session recovery. |
| [Interview capstone](references/capstone.md) | Integrated scenario design, domain examples, interview delivery, and per-gap assessment. |
| [Roadmap template](templates/roadmap.md) | Reusable learning-plan structure. |
| [Progress template](templates/progress.md) | Reusable log sheet. |
| [State template](templates/learner-state.json) | Empty structured checkpoint. |
| [Capstone brief template](templates/capstone-brief.md) | Learner-facing scenario without the solution map. |
| [Capstone assessment template](templates/capstone-assessment.md) | Assessor-only target selection, rubric, and interview record. |
| [State validator](scripts/validate_state.py) | Optional read-only bookkeeping checks. |
| [Acceptance scenarios](tests/scenarios.md) | Conversation trials for technical and mathematical topics. |

## Validation and testing

The optional tooling uses Python 3.10+ and the standard library only. From the
package directory:

```powershell
python -B -m unittest discover -s .\tests -p "test_*.py" -v
python -B .\scripts\validate_state.py .\templates\learner-state.json
```

To check a real checkpoint:

```powershell
python -B .\scripts\validate_state.py 'C:\path\to\learner-state.json'
```

The validator checks references, recorded sessions, adaptive placement budgets,
and weakness bookkeeping.
It cannot establish that an explanation is scientifically correct, a problem
is genuinely fresh, whether a capstone semantically covers its selected gaps,
or the learner really worked independently. Optional capstone metadata is not
automatically validated. Use the
acceptance scenarios to evaluate tutoring behavior and save only anonymized
observations when sharing results.
