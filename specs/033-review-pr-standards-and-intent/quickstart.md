# Quickstart: validating spec 033

## 1. Automated checks (every change)

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

Expected: all pass. `--dry-run` confirms that `extension.yml` and `catalog.json` agree on 1.22.0 and that the
zip matches `spectra/`.

## 2. No prose copy left behind

```bash
grep -n -i "baseline\|supporting doc\|older spec" AGENTS_LIST.md spectra/README.md docs/index.html
```

Expected: each of the three files has a hit in its review-pr section (R9).

## 3. Manual scenarios (throwaway repository, `specify extension add --dev ./spectra`)

| # | Set-up | Expected review | Spec ref |
|---|---|---|---|
| A | Base has `specs/001/spec.md` (default timeout 30s). PR ships `specs/002/spec.md` changing it to 60s, plus the code | No finding asks to restore 30s. If 002 names 001 and 001 is untouched: at most one Minor, with no suggestion | US1, SC-001 |
| B | No constitution. `docs/TEST_STRATEGY.md` requires integration tests for handlers. PR adds a handler with no test | A finding quoting TEST_STRATEGY.md. Coverage: "no constitution — supporting docs, conventions, baseline" and the remedy commands | US2 |
| C | No constitution, no docs. PR swallows an exception | A finding citing B1 or B7, severity by consequence. Coverage names the remedy | US2, SC-002 |
| D | No spec, no issue. PR "refactor auth helper" also changes a default used by two callers, adds a dependency, and removes an assertion | Blast radius Major (callers found). Dependency Question. Test integrity Major. Stated-intent flags the default change | US3, SC-003 |
| E | No spec. PR changes a flag that `specs/001/spec.md` FR-003 defines | One Question citing `001` FR-003, both readings stated, no suggestion | US4, SC-004 |
| F | PR ships a spec and weakens a test | Test integrity still Major. Stated-intent "not run — traceability replaces it" | US3 #5 |
| G | Any of the above | Default proposal still blockers and majors only. `yes` publishes exactly those | SC-006 |

For each one, check that coverage names the governing tier and the intent source (SC-005).
