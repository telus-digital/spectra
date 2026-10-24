# Quickstart: validating the interactive Domain Analyzer

## 1. Automated checks (repository root)

```bash
python3 -m unittest discover -s tests
python3 tools/generate_agent_docs.py --check
python3 tools/ship.py --dry-run
```

Expected: all tests pass; listings match `agents-list.json`; catalog parity, description parity, and
zip-matches pass; nothing pushed. The contract in
[contracts/domain-analyzer-behaviour.md](./contracts/domain-analyzer-behaviour.md) maps each behaviour to its
test.

## 2. Manual runs in a throwaway Spec Kit project

Install the working copy: `specify extension add --dev <path-to>/spectra/spectra` (Constitution, Development
Workflow step 5), then restart the agent.

### A — Brownfield, no constitution (the typical run)

Use any small existing codebase with no `.specify/memory/constitution.md`. Run
`/speckit-spectra-domain-analyzer`.

Expect, in order:
1. First line: constitution none found, goal generate.
2. The round announced once, then "Question 1 of 8" — the domain — with four options incl. recommended and Skip.
3. Questions 2–8, one per turn, each listing numbered candidates with `observed`/`aspirational` and a file path.
4. No `docs/DOMAIN_ANALYSIS.md` until after question 8.
5. The file: seven lens sections, every candidate with its decision, a Constitution input section with exactly
   what was accepted.
6. A create prompt for `/speckit-constitution`, not invoked.

Answer one lens with Skip and another with free text ("2.1 only, reword it to SHOULD") and check both decisions
in the file.

### B — Existing constitution, re-run

Run the create prompt from A, then re-run the analyzer. Expect: first line says found + update; each question
offers last run's answer; declined items are not offered; accepted items now in the constitution show
`status: adopted` and are absent from Constitution input; the handoff is the amend prompt, or none if empty.

### C — Legacy checkbox file

Place a 1.22.0-format file (some `- [x]`, some `- [ ]`) at `docs/DOMAIN_ANALYSIS.md` and run. Expect: ticked
items accepted; unticked items offered again in their lens marked "unticked in the earlier version"; IDs kept;
file rewritten in the new format; the report says so.

### D — Non-interactive

Run with `--non-interactive`. Expect: no questions; every candidate `not_asked`; empty Constitution input; no
`/speckit-constitution` line.
