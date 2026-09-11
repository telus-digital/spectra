# Contract: The `/speckit-plan` Handoff

**Emitted by**: `speckit.spectra.test-plan` at the end of a successful run.

## What it is

Printed text. One ready-to-copy invocation naming the written plan and stating what the planner should do
with it.

```text
/speckit-plan Plan this feature against the approved test plan at
specs/<feature>/test-plan.md. Every P1 test condition in it must map to a task that
writes the test before the implementation it covers.
```

## What it is not

| Not | Why |
|---|---|
| An invocation | The command prints it; the user runs it. Nothing is executed |
| A hook | No `before_plan` registration. A hook would make every project that installs Spectra prompt for a test plan on every feature — the opposite of the opt-in add-on this is |
| An edit to `/speckit-plan` | It is a Spec Kit core command. Spectra neither owns it nor may edit it (Principle II) |
| A marker written into `spec.md` | The input is read-only (FR-018), and a Spectra-specific line has no business in an artifact under stakeholder review |
| A dependency | `/speckit-plan` works exactly as it does today for anyone who never runs this command |

## Agent-agnosticism

The contract names the **Spec Kit command**, not an agent's spelling of it. Each agent renders its own
slash-command syntax at install time, so the command text presents this as "the planning command, which
you run" rather than hard-coding one agent's invocation. This is the posture
`speckit.spectra.test-strategy` already uses for `/speckit-constitution`.

## Why printed text is sufficient

`/speckit-plan` takes free-form `$ARGUMENTS` and reads the feature directory. A path plus one sentence of
intent is genuinely all it needs — there is no mechanism to build, and the only reliable way to make a
*core* command aware of an optional add-on's output is for the user to tell it.

## What the handoff must contain

| Element | Rule |
|---|---|
| The written path | Project-relative, exactly as written |
| The obligation | That P1 conditions become tasks, and that the test precedes the implementation |
| Nothing conditional | It is emitted on every successful write, not only when the user asks |

## When it is not emitted

| Situation | Instead |
|---|---|
| No argument was supplied | The request for a specification path |
| The run stopped at either gate | The reason it stopped |
| An existing plan was not rewritten | What exists, and what would have changed |

A run that wrote nothing never emits a handoff for a file it did not produce.
