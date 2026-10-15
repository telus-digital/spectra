# UAT Report — [FEATURE / SPEC NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.uat`. It runs after implementation, only on an explicit
    request, and records what happened when the agent performed a feature's user-acceptance scenarios.
    It is rewritten on every run; the run log at the bottom keeps the history.
  - Fill every [PLACEHOLDER]. Delete any section that genuinely does not apply — remove it entirely
    rather than leaving "N/A". The command honours what this template says: a section you delete stays
    deleted, and the command notes the omission instead of putting it back.
  - THIS REPORT CARRIES NO CHECKBOXES. The UAT tasks in `tasks.md` are the tracker; this report is the
    record behind each tick.
  - What this template CANNOT change: a scenario is marked passed only when its outcome was observed; a
    pass links its evidence; human-only, failed, and blocked scenarios stay open with a reason; no secret
    is reproduced in evidence or here; and what was read and what was run are always stated. Those rules
    live in the command, not here.
  - HTML comments like this one are guidance and are stripped from the output.
-->

| | |
|---|---|
| **Feature** | [project-relative path to the feature directory] |
| **Build under test** | [branch, plus a committed version and its source, or "working tree, no version committed"] |
| **Environment** | [locally started build, or the environment the user named] |
| **Date** | [YYYY-MM-DD HH:MM] |

---

## Scenarios

<!--
  One row per UAT scenario in the test plan. Outcome is one of: passed, failed, blocked, awaiting human,
  already done. Evidence is a project-relative path under specs/<feature>/uat/<run-stamp>/, or "—" where
  nothing was captured, with the reason saying why.
-->

| ID | Verifies | Executor | Outcome | Evidence | Reason |
|---|---|---|---|---|---|
| UAT1 | [US1-AC1] | [agent / human / either] | [outcome] | [path, or "—"] | [what was observed, or why not attempted] |

---

## Totals

- **Passed**: [n]
- **Failed**: [n]
- **Blocked**: [n]
- **Awaiting human**: [n]
- **Already done**: [n]

---

## Tools and run

<!-- What you could drive, and what you started — so a reader can reproduce or distrust it. -->

- **Tools relied on**: [the tools available in this session that operated each surface]
- **Started**: [the exact command, and the confirmation given; or "nothing — declined / non-interactive"]

---

## Withheld

<!-- Every capture masked or skipped because it might show a secret. "Nothing" is a valid answer. -->

- [scenario — what was withheld and why]

---

## Run log

<!-- One line per run, oldest first. Carried forward from the previous report; never truncated. -->

| Run | Attempted | Passed | Failed | Blocked | Evidence folder |
|---|---|---|---|---|---|
| [YYYYMMDD-HHMMSS] | [n] | [n] | [n] | [n] | [specs/<feature>/uat/<run-stamp>/] |

---

## Sources consulted and coverage

- **Read**: [tasks.md, test-plan.md, the strategy's evidence rule, the constitution, the files that named
  the start command]
- **Could not read**: [path — reason, or "nothing"]
- **Modified**: only the `[UAT]` lines in `tasks.md` that are marked passed above, plus this report and
  the evidence folder.
