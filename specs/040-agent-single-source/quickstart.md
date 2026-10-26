# Quickstart: validating the single source

Run every command from the repository root on this branch, with Python 3.9 or newer (`python3`).

## 0. Baseline

```bash
python3 -m unittest discover -s tests
python3 tools/ship.py --dry-run
```

**Expected**: both pass before and after the change.

## 1. The roster file is unchanged (US3, SC-003)

```bash
git show main:agents-list.json > /tmp/roster-before.json
python3 tools/generate_agent_docs.py
cmp /tmp/roster-before.json agents-list.json && echo identical
python3 -c "import sys; sys.path.insert(0,'.'); from spectra_cli import roster; r=roster.load(); print(len(r.agents), len(r.shipped()))"
```

**Expected**: `identical`, then `55 14`. The `spectra agent-list` tests in `tests/test_agent_list.py`
pass.

## 2. One edit, every output (US1, SC-001)

1. Change one word in the lead paragraph of `agents/adr.md`.
2. Run `python3 tools/generate_agent_docs.py --check`.
   **Expected**: exit 1, naming `AGENTS_LIST.md`, `spectra/README.md` and
   `docs/getting-started/agents.html`.
3. Run `python3 tools/generate_agent_docs.py`, then `git diff --stat`.
   **Expected**: exactly `agents/adr.md` plus those three outputs changed.
4. Change `summary:` instead and run the generator again.
   **Expected**: only `agents-list.json` and the Commands table in `spectra/README.md` change. The
   README table shows titles, not summaries.
5. Revert with `git checkout -- .`.

## 3. A hand edit is caught (US1 scenario 4, SC-005)

Edit a sentence inside the ADR card in `docs/getting-started/agents.html`, then run `--check`.

**Expected**: exit 1, naming that file. Revert.

## 4. Adding an agent (US2, SC-002)

1. Copy `agents/uat.md` to `agents/demo.md`. Set `id: demo`, `command: speckit.spectra.demo`, and
   `order: 45`.
2. Run `--check`.
   **Expected**: a failure saying the manifest does not register `speckit.spectra.demo` (FR-019).
3. Change it to `status: planned` and delete the body and the `manifest:` line, then run the
   generator.
   **Expected**: `demo` appears in `agents-list.json` and in the roadmap of `AGENTS_LIST.md`, and
   nowhere else.
4. Delete `## Examples` from a shipped agent's file and run the generator.
   **Expected**: exit 1, reporting `agents/<id>.md:<line>: missing required section "Examples"`, and
   nothing written.
5. Revert.

## 5. Unsupported Markdown is refused (US4 scenario 4)

Add `<b>x</b>` outside backticks to any shipped agent's lead, then run the generator.

**Expected**: exit 1 with `agents/<id>.md:<line>` and nothing written. Repeat with `> quote` and
`### Heading`, with the same result.

## 6. The Agent reference page (US4, SC-006)

```bash
python3 -m http.server 8791 --directory docs
```

Open `http://localhost:8791/getting-started/agents.html` with JavaScript disabled.

**Expected**:
- 14 sidebar links and 14 cards.
- Each card's "Full reference" opens in place and shows the same text as that agent's section of
  `AGENTS_LIST.md`.
- No horizontal scroll at 375 px.

## 7. Narrative pages are guarded (FR-024)

Replace one `speckit.spectra.adr` in `docs/e-learning/module-1.html` with `speckit.spectra.adrx`,
then run `--check`.

**Expected**: exit 1, naming the page and `speckit.spectra.adrx`. Revert.

## 8. Seeding is accounted for (FR-016)

Open `specs/040-agent-single-source/seeding-report.md`.

**Expected**: one section per shipped agent, listing every sentence from the old copies that did not
carry over verbatim, each marked dropped, reworded or merged.

## 9. Ship pre-flight

```bash
python3 -m unittest discover -s tests
python3 tools/checks.py --all
python3 tools/ship.py --dry-run
```

**Expected**: everything passes. `zip-matches` passes only after `tools/build_package.py` has run,
because the README and description lines inside `spectra/` changed.
