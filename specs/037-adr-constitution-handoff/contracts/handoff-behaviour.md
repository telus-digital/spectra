# Contract: ADR Handoff Behaviour

Numbered behaviours. Each one maps to the requirement it implements and the test that pins it. Tests are
text assertions over the command files, in the house style of `tests/test_*_flow.py`.

## ADR agent (`spectra/commands/adr.md`)

### The invariant

| # | Behaviour | FR | Test |
|---|---|---|---|
| A1 | A "never does" list states it never writes `.specify/memory/constitution.md` — not on approval, not when missing, not when the user insists — and why (`/speckit-constitution` owns version, impact report, propagation) | FR-001 | `test_adr_flow`: invariant and reason present |
| A2 | The same list states it never invokes `/speckit-constitution` | FR-002 | `test_adr_flow` |
| A3 | No sentence in the command offers to edit, modify, or update the constitution file (the old "Offer to make the edit" / "Only modify … if the user agrees" text is gone) | FR-001 | `test_adr_flow`: forbidden phrases absent |

### Drafting

| # | Behaviour | FR | Test |
|---|---|---|---|
| A4 | The significance test is unchanged (three bullets) | FR-020 | `test_adr_flow`: the three conditions present |
| A5 | The constitution is read semantically; the five check states (data-model) are named; `embedded` quotes the clause and drafts nothing | FR-005 | `test_adr_flow` |
| A6 | A contradiction is surfaced as a finding and drafted as `amends:`; never a clause that silently overrides | FR-005 | `test_adr_flow` |
| A7 | A superseding ADR drafts `amends:` against the principle the superseded ADR introduced | FR-006 | `test_adr_flow` |
| A8 | The record format and key order match data-model; ID is `adr-NNN-<section-slug>-<hash>`, frozen, kept on reword | FR-003, FR-004 | `test_adr_flow`: format block and ID rule |

### The gate

| # | Behaviour | FR | Test |
|---|---|---|---|
| A9 | Every drafted record is shown, then one question with the five outcomes; decline-all → `skipped`; no answer / non-interactive → `not_asked`; silence adopts nothing | FR-007 | `test_adr_flow` |
| A10 | The gate does not count against the five clarifying questions | FR-020 | `test_adr_flow` |

### Sibling ground

| # | Behaviour | FR | Test |
|---|---|---|---|
| G1 | The ADR agent's own ground is stated: architecture-level choices (datastores, messaging and eventing, architecture style, service and data boundaries, layering, integration patterns), architectural decisions on security, data handling, or reliability, and unowned conventions; ground shared with domain-analyzer is governed clause by clause | FR-010 | `test_adr_flow` |
| G2 | The four referral rows (owner + ground) are listed; nothing is drafted on them | FR-008 | `test_adr_flow`: each owner and ground named |
| G3 | For referred ground: name the owner, say whether its document exists, suggest re-running it; read only `accepted` records of an existing document and name a contradicted one; a `Superseded` or `Deprecated` ADR's records count only as the principle a supersession amends | FR-009 | `test_adr_flow` |
| G4 | A decision mixing architecture-level and language/framework parts drafts only the former | FR-008, FR-010 | `test_adr_flow` |

### Sections and handoff

| # | Behaviour | FR | Test |
|---|---|---|---|
| A11 | `## Constitution guardrails` holds every record; `## Constitution input` holds only accepted, non-adopted records, opening with check result, ADR status, goal | FR-011, FR-012 | `test_adr_flow` |
| A12 | Sections are filled where a template places them, else appended after the template's sections and noted once; a non-significant ADR gets neither | FR-013 | `test_adr_flow` |
| A13 | Sections are added to the ADR written in Step 6 of the same run; no other file is written | FR-013, Principle VII | `test_adr_flow` |
| A14 | With a constitution and ≥ 1 accepted record: one amend line naming the resolved ADR path and asking for the ADR to be cited; "nothing reaches the constitution until that command runs" | FR-014 | `test_adr_flow`: the line template |
| A15 | Nothing accepted → one sentence, no line | FR-014 | `test_adr_flow` |
| A16 | No constitution → goal `pending`, records kept, no line, `speckit.spectra.domain-analyzer` named first, later amend explained | FR-015 | `test_adr_flow` |
| A17 | A `Proposed` ADR still hands off, with the advice to run once accepted | Edge case | `test_adr_flow` |
| A18 | Step 8 lists the ADR (and a superseded ADR it edited), never the constitution | FR-016 | `test_adr_flow`: constitution absent from Step 8 |

### Unchanged

| # | Behaviour | FR | Test |
|---|---|---|---|
| A19 | Context gathering, five-question limit, numbering, template stack, artifact-root rules, supersession unchanged | FR-020 | existing `test_doc_output_paths`, `test_document_templates` pass unchanged |

## methodology (`spectra/commands/methodology.md`)

| # | Behaviour | FR | Test |
|---|---|---|---|
| M1 | The sibling-ground table has a row: architecture-level choices → `speckit.spectra.adr` — `<artifact-root>/adr/` | FR-017 | `test_methodology_flow`: `OWNERS` gains adr |
| M2 | "Five agents feed the constitution"; no "four agents" remains | FR-018 | `test_methodology_flow` |
| M3 | The ordered feeder list after the handoff does not include `speckit.spectra.adr` | FR-018 | `test_methodology_flow` |

## domain-analyzer (`spectra/commands/domain-analyzer.md`)

| # | Behaviour | FR | Test |
|---|---|---|---|
| D1 | Lens 5's ground is languages, frameworks, runtimes, dependency policy; architecture-level choices belong to `speckit.spectra.adr` | FR-019 | `test_domain_analyzer_flow` |
| D2 | Step 1 reads `<artifact-root>/adr/` Constitution input sections, accepted records only, from ADRs whose status is `Proposed` or `Accepted`; `Superseded` and `Deprecated` ADRs never constrain it | FR-019, C1, U2 | `test_domain_analyzer_flow` |
| D3 | On every lens except Technology & dependency policy it cites an accepted ADR record that covers a clause instead of drafting it; a clause no record covers may be drafted from observation | FR-019, C1, U1 | `test_domain_analyzer_flow` |
| D4 | Lenses, question count (7), and handoff otherwise unchanged | — | existing `test_domain_analyzer_flow` passes |

## Release surfaces

| # | Behaviour | Principle | Test |
|---|---|---|---|
| R1 | `extension.yml` and `catalog.json` at 1.26.0; `[1.26.0]` in CHANGELOG | V, VI | `test_extension` (version sync), `tools/ship.py --dry-run` |
| R2 | Zip rebuilt from `spectra/` | V | `test_extension` / build check |
| R3 | Generated regions unchanged | V | `generate_agent_docs.py --check` |
| R4 | No prose still says the ADR agent edits or offers to edit the constitution | V | `test_adr_flow`: scan of `AGENTS_LIST.md`, `docs/index.html` ADR card |
