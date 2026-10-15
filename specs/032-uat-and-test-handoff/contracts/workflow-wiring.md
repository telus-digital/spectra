# Contract: workflow wiring — hooks and the plan.md handoff

Covers FR-040 to FR-044 and FR-050 (the hook only).

## Manifest `hooks` block

```yaml
hooks:
  after_specify:
    command: speckit.spectra.test-plan
    optional: true
    prompt: "Generate a test plan for this spec? Pass the spec file path this specify run just wrote (its SPEC_FILE) as the argument."
    description: "Offer a stakeholder test plan right after the specification is written"
  after_implement:
    - command: speckit.spectra.uat
      optional: true
      priority: 5
      prompt: "Run UAT now? The agent performs the scenarios it can drive and leaves the rest for a human."
      description: "Offer agent-run UAT after implementation, before a PR is opened"
    - command: speckit.spectra.create-pr
      optional: true
      priority: 10
      prompt: "Open a pull request for this spec?"
      description: "Offer to open a PR after implementation completes"
```

- Both new hooks are `optional: true`. A test asserts that neither is ever `optional: false`.
- The order of `uat` before `create-pr` is asserted by position and by priority.
- The test-plan prompt never says the path was "reported above". Core specify emits its hooks block
  *before* its Completion Report, so the path has not been printed yet when the offer appears. It names
  the file the run wrote instead.

## test-plan: what replaces "Not a hook"

- Pinned: "**offered by an optional hook after specify**" and "**the hook only asks**".
- Pinned (unchanged): "never infer which specification was meant". A hook invocation with no path stops,
  exactly like an empty one. Pinned: "**reached through the hook or not**".

## The planning prompt (Step 15)

test-plan emits the prompt below after it writes the plan, and only then. It is rendered as a link to the
written path, followed by one block to copy.

```text
Next: review [test-plan.md](specs/NNN-feature/test-plan.md), then run:

<planning command> Plan this feature against the approved test plan at specs/NNN-feature/test-plan.md.
Add a "Testing obligations" section to plan.md that names that file and requires:
(1) every P1 test condition maps to a task that writes the test before the implementation it covers;
(2) each condition is tested at the level the test plan assigns;
(3) the tests listed under Regression scope stay green;
(4) every UAT scenario becomes one task in a final phase titled
"User Acceptance (UAT) — not executed by the implement command", formatted
"[UAT] UAT<n> (<verifies>) <journey> — executor: <executor>".
```

- Clause (4) is omitted when the plan has no UAT section, and clause (3) when it has no Regression scope.
  The emitted prompt never mentions a section the plan does not have.
- Pinned: "Testing obligations", and "not executed by the implement command". The phrase names the command by role, never by one agent's slash syntax (Principle III).
- Still printed and never invoked. Pinned (unchanged): "something the **user** runs".
