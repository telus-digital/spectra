# Test Plan — [FEATURE / SPEC NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.test-plan`, which runs after the specification exists
    and before the implementation is planned. It states what will be verified for one feature, so
    stakeholders can approve the tests before anyone writes them.
  - Fill every [PLACEHOLDER]. Delete any section that genuinely does not apply — remove it entirely
    rather than leaving "N/A". The command honours what this template says: a section you delete stays
    deleted, and the command notes the omission instead of putting it back.
  - THIS DOCUMENT CARRIES NO CHECKBOXES. Not in exit criteria, not anywhere. It is approved, not
    tracked — `tasks.md` is what records whether the bar was met. A checkbox reintroduced into this
    file is rendered as a plain statement by the command.
  - What this template CANNOT change: every acceptance criterion reaches a condition or the
    not-covered list; every condition names what it verifies; an ambiguous requirement gets a stated
    gap rather than an invented condition; a coverage claim cites a test file and an absence claim
    cites the search; no secret value is reproduced; and coverage of the analysis is always stated.
    Those rules live in the command, not here.
  - HTML comments like this one are guidance and are stripped from the output.
-->

| | |
|---|---|
| **Spec** | [project-relative path to the specification] |
| **Build under test** | [branch, plus a committed version and its source, or "working tree, no version committed"] |
| **Author / Date** | [name] / [YYYY-MM-DD] |

---

## 1. Scope

<!--
  Out of scope matters more than in scope. It is the line you point at later when someone asks why a
  bug wasn't caught — so every exclusion names who covers it, or says that nobody does.
  Give the user story titles here once, so USn-ACn references in section 3 are legible.
-->

**In scope**

- [behaviour or component being verified]

**Out of scope**

- [what this plan deliberately does not cover] — covered by [who, or "nobody"]

**Stories referenced in this plan**

- **US1** — [title]

---

## 2. Risks

<!--
  This section decides where the effort goes. Two to five rows. If everything is High/High, the
  exercise has failed — the ratings are derived from stated triggers, not from how severe a risk
  feels, and "accept" is a legitimate response that must appear where the rating does not justify
  effort.
-->

| Risk | Likelihood | Impact | Testing response | Trigger |
|---|---|---|---|---|
| [what could break] | H/M/L | H/M/L | [deeper coverage / extra scenario / accept] | [the condition that produced the rating] |

---

## 3. Test Conditions

<!--
  One row per thing that must be true. Conditions, not test scripts — no step sequences.
  "Verifies" is the traceability: every acceptance criterion appears at least once, and every row
  traces back to a real specification item using that item's own identifier.
  "Level" pushes each check to the cheapest place it can live, using this project's own lens names.
-->

| ID | Condition | Verifies | Level | Priority | Already covered |
|---|---|---|---|---|---|
| T1 | [what must be true, one line] | [FR-001 / SC-002 / US1-AC1] | [level] | P1 | [test path, or "—"] |

**Levels in use**: [the resolved vocabulary] — from [the strategy document's path / the constitution / convention]

**Explicitly not covered**

| Verifies | Reason | Remedy |
|---|---|---|
| [specification item] | [unresolved clarification / untestable as written / out of scope / deferred] | [what would resolve it] |

---

## 4. Environment & Data

<!-- If someone else cannot run these tests from this section alone, it is too thin. -->

- **Environment**: [where tests run; which dependencies are stubbed and which are real]
- **Test data**: [fixtures, accounts, seed state, and how it is reset]
- **Prerequisites**: [flags, migrations, access, third-party sandboxes]

---

## 5. Exit Criteria

<!--
  The bar for a go/no-go call, as plain statements — no checkboxes. Each one carries its threshold and
  the role who confirms it. The plan is done when someone can make the call from this list.
-->

| Criterion | Threshold | Confirmed by |
|---|---|---|
| [what must hold] | [the bar, numeric where the spec allows] | [role] |

---

## Sources consulted and coverage

<!--
  A reader must be able to tell "checked and found nothing" from "did not check".
-->

- **Read**: [what was read, by path, and the selection method]
- **Coverage**: [n of m relevant files read]
- **Could not read**: [path — reason, or "nothing"]
- **Nothing was executed**: existing coverage was established by reading test source, not by running
  the suite.

<!--
  OPTIONAL SECTIONS — AUTHORING GUIDANCE, NOT OUTPUT.
  Skip these by default. The command adds one only when its trigger actually fires, and says which it
  added and why. This list never appears in the generated document.

  | Section | Add when |
  |---|---|
  | Non-functional targets | The spec or constitution states a performance, security, or a11y budget |
  | Rollback / migration testing | A schema change, data migration, or backfill is implied |
  | Roles & responsibilities | A separate QA function, or more than one executing team, is named |
  | Approvals / sign-off | The constitution declares a regulated or audited regime |
  | Schedule & milestones | NEVER added automatically — project management, not test design |
  | Suspension / resumption criteria | NEVER added automatically — same reason |
  | Test summary report | NEVER added automatically — it reports an outcome; this states intent |
-->
