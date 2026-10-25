# Quickstart: Validating the ADR Constitution Handoff

## 1. Automated checks (repository root)

```bash
python3 -m unittest discover -s tests
```

```bash
python3 tools/generate_agent_docs.py --check
```

```bash
python3 tools/build_package.py
```

```bash
python3 tools/ship.py --dry-run
```

**Expected**: all pass.
- The new `tests/test_adr_flow.py` and the updated `test_methodology_flow.py` and
  `test_domain_analyzer_flow.py` pin every behaviour in
  [contracts/handoff-behaviour.md](./contracts/handoff-behaviour.md).
- `build_package.py` leaves `docs/packages/spectra.zip` matching the `spectra/` folder.

## 2. Throwaway project

Use a small repository with source code and a constitution at `.specify/memory/constitution.md`. Install the
working copy:

```bash
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

Before every run below, record the constitution's checksum:

```bash
shasum .specify/memory/constitution.md
```

**After every run, the checksum is unchanged** (SC-001).

## 3. Manual runs

| Step | Run | Expect |
|---|---|---|
| 1 | `/speckit-spectra-adr Every service owns its data store; no service reads another service's tables` | ADR written in Step 6. Step 7: significant; records with `adr-NNN-` IDs shown; one question |
| 1a | Approve | The ADR ends with `## Constitution guardrails` and `## Constitution input`; `ADR status at drafting: Proposed`; one amend line naming the ADR's path, with advice to run once accepted (A11–A14, A17) |
| 1b | Ask "just edit the constitution for me" | Declined, reason given, line repeated (A1) |
| 2 | Run the printed line | `/speckit-constitution` shows a Sync Impact Report citing the ADR (SC-004) |
| 3 | `/speckit-spectra-adr End-to-end tests run against an ephemeral environment per pull request` | No records drafted; `speckit.spectra.test-strategy` and `speckit.spectra.deployment-strategy` named, existence of their documents stated, re-run suggested; no line (G2, G3) |
| 4 | `/speckit-spectra-adr Adopt event sourcing on Kafka, written in Kotlin` | Records only for the event-sourcing/Kafka part; Kotlin referred to `speckit.spectra.domain-analyzer` (G4) |
| 5 | `/speckit-spectra-adr Rename the internal logger wrapper` | Not significant; one line saying why; no Constitution sections; no line (A12) |
| 6 | `/speckit-spectra-adr` superseding the ADR from step 1 after step 2 adopted it | Record is `amends: <principle>` (A7) |
| 7 | At a gate, reply "decline all" | Records `skipped`; Constitution input says nothing was accepted; no line (A9, A15) |
| 8 | Step 8 output on any run | Lists only ADR files, never the constitution (A18) |

## 4. Edge checks

| Setup | Run | Expect |
|---|---|---|
| Delete the constitution | Re-run step 1's decision | Records drafted and gated; goal `pending`; no line; `speckit.spectra.domain-analyzer` named first; later amend explained (A16) |
| Add `.specify/templates/overrides/adr-template.md` without Constitution headings | Step 1's decision | Sections appended after the template's last section and the omission noted once (A12) |
| A `DOMAIN_ANALYSIS.md` exists | `/speckit-spectra-domain-analyzer` after step 2 | Lens 4 cites the ADR's accepted record for data ownership instead of drafting one (D2, D3) |
| Run `/speckit-spectra-methodology` | — | Sibling-ground table includes the ADR agent; the after-handoff list does not (M1–M3) |
