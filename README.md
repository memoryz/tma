# Teach Me Anything

A portable Agent Skill for learning science, technology, engineering, and
mathematics through adaptive, research-backed tutoring.

Designed for professionals with day jobs: learn in short sessions, pause whenever
needed, and return after unpredictable gaps without restarting the whole course.
This is a set of instructions and supporting assets for an AI assistant, not a
standalone tutoring application.

## What the skill does

- Researches a topic, maps prerequisites, and builds a phased learning roadmap.
- Finds your existing knowledge and gaps through adaptive assessment: at most
  five rounds and twenty questions, stopping earlier when the learning route is clear.
- Teaches with plain-language mental models, examples, diagrams where helpful,
  and opportunities for follow-up questions before practice.
- Tracks specific gaps using three consecutive independent successes and the
  required evidence types, with delayed retention checks tracked separately.
- Saves progress and unfinished work so sessions can be irregular.
- Ends with a realistic, open-ended interview capstone integrating at least
  three previously learned gaps when available.

Prompts use rendered Markdown rather than raw formatting inside plain-text
dialogs. Formulas use supported math rendering or readable plain-text notation
when math support is unavailable or unknown. Three successes are a practical
progress policy, not a guarantee of permanent mastery.

## Quick start with GitHub Copilot CLI

The commands below use PowerShell syntax.

### 1. Register the complete skill

From this repository's root:

```powershell
copilot skill add .
copilot skill list
```

Register the directory containing `teach-me-anything`, not just its `SKILL.md`.
Keep the whole skill folder together: the references, templates, and optional
validator are part of the package.

### 2. Turn off Autopilot

**Use Interactive mode for learning.** In Autopilot, Copilot answers its own
questions on your behalf, treating you as unavailable and making its best guess.
That skips the learner responses needed for assessment and practice.

In an existing Copilot CLI session, run:

```text
/autopilot off
/settings askUser on
```

Alternatively, press **Shift+Tab** to cycle to Interactive mode. To start a new
session explicitly in Interactive mode:

```powershell
copilot --mode interactive
```

The skill has no documented mechanism to switch the CLI's mode itself. Stronger
skill instructions do not override Autopilot's question handling.

### 3. Start learning

Invoke the installed skill:

```text
/teach-me-anything
```

Then describe your topic, practical goal, background, and today's available time.
For example:

> Teach me database indexes. I build services but struggle to explain query-plan
> tradeoffs. I have 15 minutes today.

> Teach me derivatives deeply enough to understand gradient descent. I remember
> basic algebra but need help with the chain rule.

You can ask for broader coverage, deeper explanations, a diagram, a follow-up,
or a pause. The tutor should wait for your answers rather than simulate them.

If the skill is missing from an already-open session, try `/skills reload`.
If it is still missing, restart Copilot CLI and check `copilot skill list`.

### 4. Resume later

Accept a separate progress workspace, or use conversation-only tracking when
files are unavailable. A typical workspace is a topic folder under `.learning`
in your working directory, outside the reusable skill folder.

To continue, tell the assistant where your saved progress is:

> Use teach-me-anything to resume my calculus topic from the saved progress
> folder. I have five minutes today.

The tutor resumes unfinished work and checks relevant understanding without
penalizing absence or imposing a fixed schedule. Do not publish personal learner
records with the skill; `.learning` folders are ignored by this repository.

## Other compatible assistants

Ask an assistant that supports local instruction files to read
[SKILL.md](teach-me-anything/SKILL.md) and follow its linked instructions.
Give it access to the complete folder. Tool availability and persistence depend
on the host; a skill cannot enable a Markdown renderer or change host modes itself.

## Repository contents

- [Skill package guide](teach-me-anything/README.md): workflow, progress records,
  supporting files, and testing details.
- [SKILL.md](teach-me-anything/SKILL.md): main tutoring instructions.
- [Learning science](teach-me-anything/references/learning-science.md): research
  basis and limitations.
- [Templates](teach-me-anything/templates/roadmap.md): learning roadmap, progress
  records, and capstone materials in the same folder.
- [Conversation trials](teach-me-anything/tests/scenarios.md): manual acceptance
  scenarios for trying technical and mathematical topics.

## Validation

Tutoring does not require Python. The optional validator and automated tests
require Python 3.10+ and use only the standard library.

From the repository root:

```powershell
python -B -m unittest discover -s .\teach-me-anything\tests -p "test_*.py" -v
python -B .\teach-me-anything\scripts\validate_state.py .\teach-me-anything\templates\learner-state.json
```

These checks validate package integrity and progress bookkeeping, not scientific
correctness, actual understanding, or visual rendering in a particular host.
Use the conversation trials to evaluate tutoring behavior.
