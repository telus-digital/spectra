# Quickstart: validating "Retire the spectra CLI"

Run from the repository root on branch `043-retire-spectra-cli` unless stated otherwise. Use `python3`,
not `python`. Scenarios 1 to 6 need no GitHub write access; Scenario 7 is the maintainer's post-merge step.

## Prerequisites

- Spec Kit **1.4.5** on PATH (`specify --version`); uv; Git; `gh` authenticated (Scenarios 6 and 7)
- A scratch directory outside the repository, for example `"$TMPDIR/spectra-qs"`

## Scenario 1: a new user installs SPECTRA from the landing page (US1, SC-001)

In an empty scratch folder, run exactly the commands the rewritten `docs/index.html` shows, in order
([contracts/install-commands.md](contracts/install-commands.md) § Install). Use `--integration claude` with
`specify init` if you want to avoid the interactive picker.

Expected:
- `specify extension catalog list` shows `spectra`, install allowed
- `specify extension list` shows `spectra` at the version in `catalog.json`
- `.claude/skills/` (or the chosen agent's folder) holds 14 `speckit-spectra-*` entries
- No step used a `spectra` command

## Scenario 2: keep current and remove (US3)

In the same project:

```bash
specify self check
specify integration upgrade
specify extension update spectra        # expect "Up to date"
specify extension remove spectra        # confirm
specify extension list                  # spectra gone
```

## Scenario 3: projects with more than one agent (US3, FR-027, FR-028)

```bash
specify integration install kiro-cli
specify extension add spectra
ls .kiro/prompts | grep -c spectra      # expect 0 (default-only registration)
specify integration use kiro-cli
specify integration use claude
ls .kiro/prompts | grep -c spectra      # expect 14
specify integration status              # default is still claude
```

The docs' multi-agent text must match what you see. If a future Spec Kit registers every agent at install
time, the docs must be changed to say so (FR-028).

## Scenario 4: the e-learning commands run (US4, SC-007)

Open each page under `docs/e-learning/` and run every `specify` command in its labs against a scratch
project on 1.4.5. Module 3's lab ends with the agent offering both `/speckit-*` and `/speckit-spectra-*`
commands.

## Scenario 5: the repository is clean of the CLI (SC-002, SC-003, SC-006, SC-008, FR-008)

```bash
python3 -m unittest discover -s tests
python3 tools/checks.py --all
python3 tools/generate_agent_docs.py --check

test ! -e spectra_cli && test ! -e pyproject.toml && test ! -e VERSION && test ! -e test \
  && test ! -e .github/workflows/release.yml && echo "CLI removed"

# Forbidden commands and phrases in current docs: expect no output
# ((^|[^-])spectra-cli skips this feature's own directory name, 043-retire-spectra-cli)
grep -rnE 'spectra (install|check|version|update|uninstall|agent-list|cli)\b|(^|[^-])spectra-cli|spectra_cli|uv tool (un)?install spectra|SPECTRA_NO_UPDATE_CHECK|no-update-check|releases/latest|curated (catalog|set)|TELUS Digital platform' \
  README.md CLAUDE.md CONTRIBUTING.md SECURITY.md SHIPPING.md .specify/memory/constitution.md docs \
  --include='*.md' --include='*.html' | grep -v 'docs/ip-audit-findings.md'

# The extension did not change: expect no output
git diff main --stat -- spectra/ catalog.json docs/packages/spectra.zip agents-list.json

# Counts quoted in the brief and README match the package
ls spectra/commands | wc -l; ls spectra/templates | wc -l
```

Then read the landing page, capability brief, and getting-started overview in a browser (Pages preview or
`file://`): each describes SPECTRA per [contracts/positioning.md](contracts/positioning.md), and the
landing page shows only the "Agents v…" badge.

## Scenario 6: the required-check switch keeps main pushable (US5, FR-011, SC-005)

Follow [contracts/required-checks.md](contracts/required-checks.md) § The switch sequence. Expected:
`tools/ship.py` lands the merged SHA on `main` with every required check green, and the push output names no
bypassed status check.

## Scenario 7: maintainer retires Releases and tags (FR-007, FR-030, SC-004)

After the merge has landed on `main`:

```bash
gh release list -R telus-digital/spectra --limit 100 --json tagName --jq '.[].tagName' \
  | while read -r t; do gh release delete "$t" -R telus-digital/spectra --cleanup-tag --yes; done

git ls-remote --tags origin | awk '{print $2}' | sed 's#refs/tags/##; s#\^{}##' | sort -u \
  | while read -r t; do git push origin --delete "refs/tags/$t"; done

git tag -l | while read -r t; do git tag -d "$t"; done
```

Verify (all three print nothing or `0`):

```bash
gh release list -R telus-digital/spectra --limit 100
git ls-remote --tags origin
gh api repos/telus-digital/spectra/releases --jq length
```

Then open the landing page and confirm nothing on it broke, because it no longer reads a Release.
