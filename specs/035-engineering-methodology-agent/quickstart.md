# Quickstart: Validating the Methodology Agent

## 1. Automated checks (repository root)

```bash
python3 -m unittest discover -s tests
python3 tools/generate_agent_docs.py --check
python3 tools/build_package.py
python3 tools/ship.py --dry-run
```

Expected:
- All tests pass, including the new `tests/test_methodology_flow.py` and the updated
  `test_domain_analyzer_flow`, `test_deployment_strategy_flow`, `test_doc_output_paths`, `test_kb_vault_flow`,
  and `test_review_pr_flow`.
- `--check` reports no drift; the methodology agent has a prose block in `spectra/README.md` and
  `AGENTS_LIST.md`.
- `extension.yml` and `catalog.json` agree on 1.24.0 and 14 commands.

Behaviours pinned by these tests: [contracts/methodology-behaviour.md](./contracts/methodology-behaviour.md).

## 2. Manual run: brownfield (User Stories 1–3)

In a throwaway Spec Kit project with history, a CI workflow, and a PR template, install the extension from the
working tree and run:

```text
/speckit.spectra.methodology
```

Check:
1. The first output names `brownfield`, the signals found, and create/update.
2. Ten questions, one per turn. Adopt TDD in question 1; in question 2 accept MUST for feature and fix.
3. No file exists until question 10 is answered.
4. `docs/ENGINEERING_METHODOLOGY.md` has every section from research R12. The obligations matrix shows TDD's
   tasks-phase ordering and its `tasks.md` evidence.
5. The report ends with one `/speckit-constitution` line, then lists missing sibling agents in the order
   domain-analyzer → methodology → test-strategy → deployment-strategy.
6. Nothing under coverage, environments, or versioning is proposed; each is referred
   ([contracts/sibling-boundaries.md](./contracts/sibling-boundaries.md)).

## 3. Manual run: greenfield and non-interactive (User Stories 4–5)

- In an empty repository: the first output names `greenfield`; every candidate is `aspirational`.
- In a repository with a CI workflow, five commits, and only generator output: exactly one signal
  (workflow configuration), so a mixed reading is stated and asked before lenses.
- In a repository holding a real codebase imported as one squashed commit, with no CI: exactly one signal
  (source), so again a mixed reading (User Story 4 scenario 3).
- With a hand-written `docs/ENGINEERING_METHODOLOGY.md` already present and `--non-interactive`: the file is
  cited as evidence, left unchanged, and the document is shown in the session. No other file appears in `docs/`.
- With an `ENGINEERING_METHODOLOGY.md` this agent wrote, run `/speckit.spectra.kb-vault` on a methodology PDF: the
  plan shows a referral, not an update; the file is byte-for-byte unchanged; the report lists the source under
  "Sources referred on" and names `/speckit.spectra.methodology`.
- `/speckit.spectra.methodology --non-interactive`: no questions are asked, every candidate is `not_asked`, and
  there is no handoff line.

## 4. Re-run and migration

- Re-run after adopting guardrails through `/speckit-constitution`: answers are prefilled, adopted items are
  marked and absent from Constitution input, and declined items are not re-offered.
- With a `DOMAIN_ANALYSIS.md` from 1.23.0 that has accepted Delivery & workflow items: methodology prefills them.
  Re-running the domain analyzer keeps them under "Handed on" and asks seven questions.
