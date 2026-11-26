# Contract: required checks and the switch sequence

## After this feature (FR-009, FR-010, FR-012)

`.github/required-checks.json`, the job names in `.github/workflows/ci.yml`, and the live "Protect main —
tested" ruleset (id 23750842) all list exactly these contexts:

```json
[
  "Tests pass",
  "Catalog and package stay in sync",
  "CodeQL finds no high-severity issues"
]
```

| Context | Job id | What it runs | Notes |
|---|---|---|---|
| `Tests pass` | `tests` | checkout; `actions/setup-python` (existing pinned commit) with `python-version: '3.x'`; `python -m unittest discover -s tests -v` | **New.** No matrix, no `pip install`, so the context has no `(x.y)` suffix |
| `Catalog and package stay in sync` | `catalog` | the four `tools/checks.py` checks | Unchanged |
| `CodeQL finds no high-severity issues` | `codeql` | CodeQL init/analyze + `tools/codeql_gate.py` | Unchanged; still scans the remaining Python (`tools/`, `tests/`) and the workflows |

Removed: `CLI installs and runs (3.9)` and `CLI installs and runs (3.12)` (job `cli`), along with every step
that installed the package or asserted the banner, version, removed flags, `spectra cli` commands, or wheel
contents.

`tests/test_ci_contract.py` keeps enforcing that the workflow's contexts equal `required-checks.json`, and
must handle a job with no matrix.

## The switch sequence (FR-011, `SHIPPING.md` § The rename deadlock)

At no step may `main` require a context that the commit being pushed cannot earn.

| # | Who | Action | Check before moving on |
|---|---|---|---|
| 1 | implementation | Commit the new `ci.yml` and `required-checks.json` with the rest of the feature on the branch; merge the branch into local `main` | `python3 -m unittest discover -s tests` and `python3 tools/checks.py --all` pass |
| 2 | maintainer | `git push --force origin HEAD:refs/heads/ci` (the `ci` branch is not protected) | `gh run list --branch ci --limit 1` completes green |
| 3 | maintainer | Read the new contexts off that run: `gh api repos/telus-digital/spectra/commits/$(git rev-parse HEAD)/check-runs --jq '.check_runs[].name'` | They are exactly the three above |
| 4 | maintainer | Point the ruleset at them (see command below) | `gh api repos/telus-digital/spectra/rulesets/23750842 --jq '[.rules[] \| select(.type=="required_status_checks") \| .parameters.required_status_checks[].context]'` prints the three contexts |
| 5 | maintainer | `python3 tools/ship.py` | It reports the file and ruleset agree, waits for green on `ci`, and pushes the same SHA to `main` |

Ruleset update for step 4 (replaces the required-contexts list and keeps everything else):

```bash
gh api repos/telus-digital/spectra/rulesets/23750842 > /tmp/ruleset.json
python3 - <<'EOF'
import json
r = json.load(open("/tmp/ruleset.json"))
for rule in r["rules"]:
    if rule["type"] == "required_status_checks":
        rule["parameters"]["required_status_checks"] = [
            {"context": c} for c in json.load(open(".github/required-checks.json"))]
body = {k: r[k] for k in ("name", "target", "enforcement", "conditions", "rules", "bypass_actors")}
json.dump(body, open("/tmp/ruleset-new.json", "w"))
EOF
gh api -X PUT repos/telus-digital/spectra/rulesets/23750842 --input /tmp/ruleset-new.json
```

Between step 4 and step 5 no other ship may run. With one maintainer that only means not starting a second
change.
