# Quickstart: Validating Safe Foundation Handoffs

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
- The new `tests/test_onboarding_sequence.py` and the updated flow tests pin every behaviour in
  [contracts/handoff-behaviour.md](./contracts/handoff-behaviour.md).
- `build_package.py` leaves `docs/packages/spectra.zip` matching the `spectra/` folder.

## 2. Throwaway brownfield project

Use an existing small repository with source code, some tests, a CI workflow, and git history, and no
`.specify/memory/constitution.md`. Install the working copy:

```bash
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

Prepare outside documents:
- a test-strategy PDF or Markdown file that claims a coverage floor above what the repository measures;
- a workflow document that says "we squash-merge" in a repository whose history has merge commits.

## 3. Manual runs, in the documented order

| Step | Run | Expect |
|---|---|---|
| 1 | `/speckit-spectra-kb-vault` with both documents | The plan has rows under `docs/test-strategy-source/` and `docs/engineering-methodology-source/` that name `speckit.spectra.test-strategy` and `speckit.spectra.methodology`; no singleton row. After approval, no `TEST_STRATEGY.md` or `ENGINEERING_METHODOLOGY.md` exists (K1–K5) |
| 1a | Ask kb-vault to put the test strategy at `docs/TEST_STRATEGY.md` | Declined; the owner is named; the full table is shown again (K4) |
| 2 | `/speckit-spectra-domain-analyzer` | Goal **create**; header starts `command: speckit.spectra.domain-analyzer`; create hand-off |
| 3 | Run the printed `/speckit-constitution` line | A constitution exists |
| 4 | `/speckit-spectra-methodology` | Goal **update**; the imported workflow document is listed as an input and cited `claimed`; squash vs merge commits reported both ways, history as current practice (F4–F6) |
| 5 | Run the printed amend line | |
| 6 | `/speckit-spectra-test-strategy` | Goal **update**; the imported PDF is cited `claimed`; the floor stays at or below the baseline; a `Constitution input` section with `ts-` IDs; methodology's accepted TDD obligation cited, not re-drafted (S1, S3, S10) |
| 6a | At the gate, reply "approve, but decline the UAT clause" | The UAT record is `declined`; the others are `accepted` (S5) |
| 7 | Run the printed amend line, then re-run test-strategy | The accepted records are `adopted: …` and gone from Constitution input; the declined UAT record is not offered as new (S7) |
| 8 | `/speckit-spectra-deployment-strategy` | The same contract with `ds-` IDs |
| 9 | Confirm `docs/test-strategy-source/` and `docs/engineering-methodology-source/` | Byte-for-byte unchanged since step 1 (SC-002) |

## 4. Edge checks

| Setup | Run | Expect |
|---|---|---|
| Delete the constitution; run test-strategy | | Goal **create**; create hand-off (S2) |
| Replace `TEST_STRATEGY.md` with a 1.24.0-format file holding `- [x]` and `- [ ]` items | Re-run test-strategy | `[x]` → accepted, `[ ]` → offered again as "unticked in the earlier version"; the report says it was migrated (S8) |
| Hand-write a `DOMAIN_ANALYSIS.md` with no front matter | Run domain-analyzer | Consent asked before the round; on "no", nothing is written and the document is shown in the session (F3) |
| A 1.24.0 `DOMAIN_ANALYSIS.md` written by domain-analyzer (no `command:` key) | Run domain-analyzer | Treated as a prior run with no consent prompt; the rewrite adds the key (F2) |
| A PR touching code that a **declined** test-strategy record would flag | `/speckit-spectra-review-pr` | No finding from the declined record (P1, SC-009) |
| `--non-interactive` on test-strategy | | Every record `not_asked`; Constitution input says nothing was accepted; no hand-off command |
| A 1.24.0-format `TEST_STRATEGY.md` whose amendment has only `- [ ]` items | `/speckit-spectra-review-pr` | No standard drawn from it; the review says so plainly and does not call the file unreadable (U1) |
| `DEPLOYMENT_STRATEGY.md` holding a declined record | Run domain-analyzer | The declined record does not constrain any candidate (C1) |

## 5. Documentation check

Open `README.md`, `spectra/README.md`, and the landing page. Each has a "Starting on an existing codebase"
section with the same order, the reason the constitution runs between feeders, and the `Artifact root:`
advice (D1–D2).
