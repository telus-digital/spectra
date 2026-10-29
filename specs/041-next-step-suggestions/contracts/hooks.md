# Contract: the `hooks:` section of `spectra/extension.yml`

This is the complete section as it will ship (FR-001 to FR-010). Prompts are the user-facing contract.
Descriptions and comments may be reworded at implement time, but the facts they state may not change.

```yaml
hooks:
  # Every Spectra hook is an offer: optional, so it asks and never runs on its own. None carries a
  # condition, because Spec Kit's command templates skip any hook that has one.
  #
  # Order: Spec Kit's command templates show an event's hooks in the order they are listed here and do
  # not sort them by priority. The list order below is therefore the order users see. Each priority
  # agrees with that order so the two never disagree, but priority does not set it.
  #
  # Spectra registers hooks only after core Spec Kit commands. What follows a Spectra agent is that
  # agent's own closing suggestion, written from how its run turned out.
  after_specify:
    command: speckit.spectra.test-plan
    optional: true
    prompt: "Generate a test plan for this spec? It uses the feature this specify run just recorded, so no path is needed."
    description: "Offer a stakeholder test plan right after the specification is written"
  after_clarify:
    command: speckit.spectra.test-plan
    optional: true
    prompt: "Build or refresh the test plan from the clarified spec? It uses the feature this clarify run worked on, so no path is needed."
    description: "Offer a test plan built from the clarified specification"
  after_implement:
    # speckit.converge is a core Spec Kit command, not a Spectra one. Spec Kit shows a hook that targets
    # a core command (verified on 1.2.4), but its extension reference does not document this, so a later
    # release could stop showing this one offer. Nothing else depends on it.
    - command: speckit.converge
      optional: true
      priority: 3
      prompt: "Check the build against the spec, plan, and tasks for work that is still unbuilt?"
      description: "Offer converge after implementation, before UAT and a pull request"
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
  # Converge ends with its own next step: implement when it appended tasks, review or a PR when nothing
  # remained. In the second case nothing else offers UAT, so this does. The prompt reads correctly either
  # way, and the UAT agent's implementation-incomplete check makes an early run safe.
  after_converge:
    command: speckit.spectra.uat
    optional: true
    prompt: "Run UAT now? If converge just added tasks, finish them with implement first — UAT will tell you if any are still open."
    description: "Offer UAT after converge, so a converged feature is tested before a pull request"
```

## Invariants the tests assert

1. The event keys are exactly `after_specify`, `after_clarify`, `after_implement`, `after_converge`.
2. The commands under each event are exactly as above. Under `after_implement` they appear in the order
   converge, uat, create-pr.
3. Every entry has `optional: true`. No entry has `optional: false` or a `condition`.
4. Within `after_implement`, priorities strictly increase in list order.
5. The `after_converge` prompt equals the clarified wording exactly (FR-007).
6. No prompt names a path (`specs/`, `SPEC_FILE`).
7. The comment block states that list order, not priority, controls what users see. It contains no claim
   that Spec Kit sorts on priority.
8. `requires.speckit_version` is `>=0.11.2`.
