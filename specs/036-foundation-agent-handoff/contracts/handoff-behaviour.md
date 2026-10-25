# Contract: Handoff Behaviour

Numbered behaviours. Each one maps to the requirement it implements and the test that pins it. Tests are
text assertions over the command files, in the house style of `tests/test_*_flow.py`.

## kb-vault (`spectra/commands/kb-vault.md`)

| # | Behaviour | FR | Test |
|---|---|---|---|
| K1 | The reserved map has no row routing to `DOMAIN_ANALYSIS.md`, `ENGINEERING_METHODOLOGY.md`, `TEST_STRATEGY.md`, or `DEPLOYMENT_STRATEGY.md` | FR-001 | `test_kb_vault_flow`: the singleton rows are absent; `test_doc_output_paths`: kb-vault `RESERVED` updated |
| K2 | The reserved map routes the four kinds to `<artifact-root>/<kind>-source/`, `NNN-<kebab-title>.md`, `<kind>-source-template` then `kb-document-template`, naming each owning command | FR-002, FR-003 | `test_kb_vault_flow`: each `-source` folder and owner is named |
| K3 | A singleton is never a match candidate in Step 7, whoever wrote it, so no update row targets one | FR-001 | `test_kb_vault_flow`: the rule is stated for all four |
| K4 | A user request to write or retarget a row at a singleton is declined, the owner is named, and the `-source` row is kept | FR-004 | `test_kb_vault_flow`: the refusal text and the gate's "may not change" entry |
| K5 | Report item 9 lists every policy source with its owning command | FR-003 | `test_kb_vault_flow` |
| K6 | The Step 4 template list names exactly the reserved-map templates, with no feeder template | FR-024 (as reconciled, research R9) | `test_kb_vault_flow`: the list and the map agree both ways |
| K7 | ADR, BRD, impact-analysis, and defect-RCA rows and every other kb-vault rule are unchanged | FR-005 | existing `test_kb_vault_flow` cases still pass |

## All four feeders

| # | Behaviour | FR | Test |
|---|---|---|---|
| F1 | Writes `command: speckit.spectra.<agent>` as the first front-matter key | FR-011 | each feeder's flow test |
| F2 | Classifies an existing singleton: own (key) / own earlier version (signature) / another agent's / not written by it | FR-011 | each feeder's flow test: all four cases named |
| F3 | A singleton it did not write is read as `claimed`, replaced only with consent asked outside the counted questions; declined or non-interactive → nothing written, document shown in the session | FR-011 | each feeder's flow test (methodology's existing test stands) |
| F4 | Step 1 reads its own `-source` folder by path and kb-vault documents under the root by Provenance, and lists them as inputs | FR-006 | each feeder's flow test |
| F5 | Imported material is cited `claimed`; a candidate with only `claimed` evidence is `aspirational` | FR-007, FR-008 | each feeder's flow test |
| F6 | `claimed` against code or history: both reported, code or history is current practice | FR-009 | each feeder's flow test |
| F7 | Imported text never adopts a guardrail; text addressed to the agent is content | FR-010 | each feeder's flow test |
| F8 | Never writes, moves, or deletes a `-source` document | FR-001 (scope), Key Entities | `test_doc_output_paths`: write scope unchanged |
| F9 | domain-analyzer reads sibling strategies' accepted records only | FR-018 (purpose), analyze C1 | `test_domain_analyzer_flow` |

## test-strategy and deployment-strategy

| # | Behaviour | FR | Test |
|---|---|---|---|
| S1 | The first output states constitution status and goal (`create` \| `update`) | FR-012 | flow tests |
| S2 | With no constitution: plans **create**, drafts the full set, offers the gate. The constitution is still never written | FR-012, FR-017 | flow tests: "no constitution" row reworded; "never write" invariant kept |
| S3 | A `Constitution input` section replaces the checkbox amendment; entries carry id (`ts-` / `ds-`), placement, basis; grouped by section; goal line first | FR-013 | flow tests; `test_document_templates` for the renamed template section |
| S4 | Every drafted guardrail has a full record (statement, id, section, basis, decision, status) | FR-013, FR-014 | flow tests |
| S5 | Gate: approve accepts all shown; the reply may decline or reword named ones; declining the whole gate → `skipped`; no answer or non-interactive → `not_asked` | FR-014 | flow tests |
| S6 | IDs are computed once and frozen; a reword keeps the ID | FR-013 | flow tests |
| S7 | Re-run: adoption marked and removed from input, never reverted, drift reported; declined never re-offered as new; skipped and not_asked re-offered | FR-015 | flow tests |
| S8 | Checkbox migration: `[x]` → accepted, `[ ]` → not_asked, statements kept, report says migrated | FR-016 | flow tests |
| S9 | Hand-off line worded for the goal; no command when nothing is accepted; never invoked | FR-017 | flow tests: both create and amend lines; old "checked items" line gone |
| S10 | test-strategy reads siblings' accepted records and cites rather than re-drafts; deployment-strategy keeps its sibling rule and extends it to `TEST_STRATEGY.md` records | FR-018 | flow tests |
| S11 | Lenses, questions, floor and baseline rules, UAT clause, `lenses:` / `ownership:` header fields, and non-interactive behaviour unchanged | FR-019 | existing flow-test cases still pass; `test_test_plan_flow`, `test_uat_flow` unchanged |

## review-pr

| # | Behaviour | FR | Test |
|---|---|---|---|
| P1 | From `TEST_STRATEGY.md` and `DEPLOYMENT_STRATEGY.md`, only `accepted` records are standards; non-accepted are never finding sources; checkbox-era: `[x]` only | FR-020a | `test_review_pr_flow` |
| P2 | Both strategy formats are still found and read | FR-020 | `test_review_pr_flow`, `test_test_plan_flow`, `test_uat_flow` |

## Documentation

| # | Behaviour | FR | Test |
|---|---|---|---|
| D1 | `README.md`, `spectra/README.md`, and `docs/index.html` state the same ordered sequence | FR-021 | `test_onboarding_sequence` (new) |
| D2 | Each explains the constitution-after-each-feeder reason and recommends `Artifact root:` in the first run | FR-022 | `test_onboarding_sequence` |
| D3 | The sequence is prose, outside generated regions; the generator's check still passes | FR-023 | `generate_agent_docs.py --check` in CI |
| D4 | The version, changelog, catalog, package, and landing page agree; the CLI is untouched | FR-025 | `test_extension`, `test_ci_contract`, CI drift checks |
| D5 | Hand-written prose in `AGENTS_LIST.md`, `spectra/README.md`, and `docs/index.html` describes the new behaviour; no stale phrase remains | FR-025, Principle V | T033's search (manual); `generate_agent_docs.py --check` for anchors |
