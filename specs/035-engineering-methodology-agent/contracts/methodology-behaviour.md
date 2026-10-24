# Contract: `speckit.spectra.methodology` Behaviour

A command file is a prompt, so its text is the implementation. Each behaviour below must be stated in
`spectra/commands/methodology.md` (or in the named sibling file), and is pinned by a text assertion in the
named test, in the style of `tests/test_domain_analyzer_flow.py`. B-numbers are stable; tasks reference them.

## Interface

```text
/speckit.spectra.methodology [focus hint] [--non-interactive]
```

- `$ARGUMENTS`: an optional focus hint. It weights the analysis but never narrows it, so all nine lenses are
  still worked.
- `--non-interactive`: the only flag; it declares that no answer can be taken in this session.
- Writes: `<artifact-root>/ENGINEERING_METHODOLOGY.md` only.
- Reads: the repository, git history (read-only), the constitution, and sibling documents.

## Behaviours

| # | Behaviour | FR | Test (`tests/…`) |
|---|---|---|---|
| B1 | The first output names the mode, the signals found, and the goal (create/update) with the constitution's version | FR-001 | `test_methodology_flow` |
| B2 | Mode is detected from three named signals, the source signal being "more than 20 non-blank lines changed in more than one commit" (or five such files when history has at most one commit, so a squashed import counts); ≥2 means brownfield, 0 greenfield, 1 a mixed reading the team settles before lenses | FR-002 | `test_methodology_flow` |
| B3 | Reads the inputs listed in FR-003 before proposing anything | FR-003 | `test_methodology_flow` |
| B4 | Works the nine named lenses on every run; a lens with nothing to propose says what was searched | FR-004 | `test_methodology_flow` (`LENSES` tuple) |
| B5 | Lens → section mapping uses the project's names, else the R9 defaults | FR-005 | `test_methodology_flow` |
| B6 | Brownfield: current practice with citations before candidates. Greenfield: "no practice to report" and defaults | FR-006 | `test_methodology_flow` |
| B7 | Every candidate is tagged `observed`/`aspirational`; at most five per lens | FR-007, FR-008 | `test_methodology_flow` |
| B8 | Asserted candidates are suppressed; changing ones are marked `amends:` | FR-009 | `test_methodology_flow` |
| B9 | Lens 2 classifies feature, fix, refactor, docs, spike, hotfix and covers spike rules | FR-010 | `test_methodology_flow` |
| B10 | Lens 3 refers the BRD format to `speckit.spectra.brd` | FR-011 | `test_methodology_flow` |
| B11 | Lens 8 offers exactly three named autonomy levels as question 9's options, every phase a human checkpoint recommended, plus Skip; tools and secrets candidates ride with the chosen level unless free text excludes them | FR-011a | `test_methodology_flow` |
| B12 | SDD is the base, never optional; TDD, BDD/ATDD, DDD, contract-first, ADR-driven are offered with evidence | FR-012, FR-013 | `test_methodology_flow` |
| B13 | Adopted overlays carry strictness, scope, and phase obligations drawn only from the R7 matrix; each overlay is one candidate (`em-overlay-<name>`), so lens 1 holds at most five | FR-008, FR-014 | `test_methodology_flow` |
| B14 | Implement-phase obligations state their `tasks.md` evidence: the test task records a failing run before its implementation task is ticked | FR-014a | `test_methodology_flow` |
| B15 | Unpractised overlays are `aspirational` and default to new-and-changed code | FR-015 | `test_methodology_flow` |
| B16 | Process cadences never enter Constitution input | FR-016 | `test_methodology_flow` |
| B17 | Conflicting obligations at one phase are reported, and a precedence is obtained before writing | FR-017 | `test_methodology_flow` |
| B18 | Sibling ground is never proposed; it is cited or its command named, per `sibling-boundaries.md` | FR-018 | `test_methodology_flow` |
| B19 | Ten questions, "Question N of 10", one per turn, announced once with the ways out | FR-021 | `test_methodology_flow` |
| B20 | Question 2 is one overlay table with Accept all / Make every overlay SHOULD / Choose per row / Skip | FR-021a | `test_methodology_flow` |
| B21 | ≥4 options, exactly one recommended with evidence, one Skip, free text accepted | FR-022 | `test_methodology_flow` |
| B22 | A question with nothing to choose becomes a confirmation, keeping its number and four options | FR-023 | `test_methodology_flow` |
| B23 | Skip, silence, and non-interactive adopt nothing; "use your defaults" takes the recommendations | FR-024 | `test_methodology_flow` |
| B24 | One file, written only after the round, rewritten in place on re-runs | FR-025 | `test_methodology_flow`, `test_doc_output_paths` |
| B25 | The body has a mode-choice table, branch-naming and commit-prefix references, and the obligations matrix | FR-026 | `test_methodology_flow` (template sections) |
| B26 | Candidate record fields, Constitution input format, and the Decisions and sources section | FR-027–FR-029 | `test_methodology_flow` |
| B27 | Template resolved through the five-layer stack and reported; Constitution input written even if an override omits it | FR-030 | `test_methodology_flow`, `test_document_templates` |
| B28 | One `/speckit-constitution` line worded for the goal, or none | FR-031 | `test_methodology_flow` |
| B29 | Lists sibling agents not yet run, in the suggested order, after the handoff line; folds in no sibling input | FR-031a | `test_methodology_flow` |
| B30 | Never edits the constitution or other files, never runs another phase, makes no network request | FR-032 | `test_methodology_flow` |
| B31 | Never reports practice without evidence | FR-033 | `test_methodology_flow` |
| B32 | IDs `em-<lens>-<hash>` are frozen; re-runs prefill, never re-offer declined, never delete, never revert adopted | FR-035, FR-036 | `test_methodology_flow` |
| B33 | `--non-interactive` is declared, never inferred; asks nothing, records `not_asked`, gives no handoff line | FR-037 | `test_methodology_flow` |
| B35 | A hand-written file at the canonical path (no command front matter) is read as evidence; replacing it needs consent before the round; otherwise (always when non-interactive) nothing is written and the document is shown in the session; no second file is ever written | FR-025, FR-033 | `test_methodology_flow` |
| B34 | Declared artifact root, publication check, non-publishing fallback; no earlier location | FR-025, Principle VII | `test_doc_output_paths` |

## Sibling edge behaviours

| # | File | Behaviour | Test |
|---|---|---|---|
| E1 | `domain-analyzer.md` | Six lenses, seven questions ("Question N of 7"); names `speckit.spectra.methodology` for Delivery & workflow ground | `test_domain_analyzer_flow` |
| E2 | `domain-analyzer.md` | Prior Delivery & workflow records are kept under "Handed on to `speckit.spectra.methodology`" and leave Constitution input | `test_domain_analyzer_flow` |
| E3 | `domain-analysis-template.md` | No Delivery & workflow section; Decisions and sources says seven questions | `test_domain_analyzer_flow` |
| E4 | `methodology.md` | Reads carried-over `da-` records as prior answers (accepted → prefilled, declined → not re-offered, adopted → kept) | `test_methodology_flow` |
| E5 | `deployment-strategy.md` | *Release & versioning* no longer proposes the branching model, and cites `ENGINEERING_METHODOLOGY.md` or names the command | `test_deployment_strategy_flow` |
| E6 | `kb-vault.md` | Reserved-map row: engineering methodology → `<artifact-root>/ENGINEERING_METHODOLOGY.md`, `engineering-methodology-template`; series example replaced; a file with `command: speckit.spectra.methodology` front matter is never updated — kb-vault leaves it unchanged, names `/speckit.spectra.methodology`, and lists the source under "Sources referred on" in its report; a file without that front matter takes the existing update rules | `test_kb_vault_flow` |
| E7 | `review-pr.md` | T2 row for `<root>/ENGINEERING_METHODOLOGY.md`; only accepted guardrails are standards | `test_review_pr_flow` |
| E8 | constitution | Principle VII names `ENGINEERING_METHODOLOGY.md` among the singletons | `test_doc_output_paths::test_the_constitution_names_every_singleton` |
