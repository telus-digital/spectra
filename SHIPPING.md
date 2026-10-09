# Shipping Spectra

How a change gets from your working tree onto `main`, and what to do when it will not go.

This file is the procedure. [`CONTRIBUTING.md`](CONTRIBUTING.md) is how to *build* things — anatomy,
conventions, authoring a command. This is how to *land* them. If the two ever disagree, this file is
wrong, because it is the one that is meant to be complete.

## Quick reference

```bash
python tools/ship.py
```

That is the only way anything reaches `main`. Never `git push origin main`.

| What changed | Bump | Path |
| --- | --- | --- |
| A new agent, or an existing one | `spectra/extension.yml` + `catalog.json` | [Path A](#path-a--an-agent-catalog-channel) |
| `spectra_cli/` | `VERSION`, then a git tag | [Path B](#path-b--the-cli-cli-channel) |
| Docs, specs, tooling, housekeeping | nothing | [Path C](#path-c--everything-else) |
| Nothing — you just want a verdict | — | `python tools/ship.py --dry-run` |

---

# Part 1 — How the gate works

## What is checked, and where

Every quality and security check on this repository, grouped by when it fires. Everything here is
live; [the commands at the end of this section](#confirming-the-settings) show it from the API.

| When | Check | Kind | Blocks? | Defined in |
| --- | --- | --- | --- | --- |
| `ship.py` pre-flight, on your machine | Catalog drift checks | Quality | Yes, nothing is pushed | [`tools/checks.py`](tools/checks.py) |
| | The full `unittest` suite | Quality | Yes, nothing is pushed | [`tests/`](tests/) |
| Any push, including to `ci` | Secret scanning **push protection** | Security | Yes, the push is rejected | Repo settings |
| CI on the `ci` branch, required by the ruleset | `CLI installs and runs (3.9)` and `(3.12)` | Quality | Yes | `ci.yml` → `cli` |
| | `Catalog and package stay in sync` | Quality | Yes | `ci.yml` → `catalog` |
| | `CodeQL finds no high-severity issues` | Security and quality | Yes for high and critical security findings; everything else is a warning | `ci.yml` → `codeql` |
| A release tag is pushed | The tag equals `VERSION` | Release integrity | Yes, no Release is published | [`release.yml`](.github/workflows/release.yml) |
| Continuously | Secret scanning, with **validity checks** | Security | No, raises an alert | Repo settings |
| | Dependabot alerts and security updates | Security | No, raises an alert or a PR | Repo settings |
| Whenever someone reports one | Private vulnerability reporting | Security intake | — | Repo settings, [`SECURITY.md`](SECURITY.md) |

### What the required CI jobs assert

- **`CLI installs and runs`**, on Python 3.9 (the floor in `pyproject.toml`) and 3.12. It installs
  the package and runs the full test suite. It checks that the installed version and the bare
  `spectra` banner both report `VERSION`, that the removed flags name their replacements, and that
  `spectra cli version` and `spectra cli update` run outside a Spec Kit project. It also checks that the wheel ships `spectra_cli/` only (never `tools/`,
  `tests/` or `agents-list.json`), and that bare `spectra` writes nothing to the current directory.
- **`Catalog and package stay in sync`** runs the four checks in `tools/checks.py`, the same code the
  pre-flight runs: the generated listings match `agents-list.json`; `extension.yml`, `catalog.json`
  and the zip agree; every published copy of the description agrees; and the zip matches `spectra/`.
- **`CodeQL finds no high-severity issues`**: see [the CodeQL check](#the-codeql-check).

### How the pipeline itself is hardened

- **Every action is pinned to a commit**, with its version in a trailing comment. A tag can be moved
  to different code; a commit cannot. Nothing updates the pins automatically. To move one, resolve
  the new tag to its commit and replace the SHA and the comment:
  ```bash
  gh api repos/actions/checkout/git/ref/tags/v4.4.0 --jq .object
  ```
  If that prints `"type": "tag"`, it is an annotated tag; resolve it once more with
  `gh api repos/<owner>/<repo>/git/tags/<sha> --jq .object.sha`.
- **The workflow token is read-only by default.** `ci.yml` sets `contents: read`. Only the `codeql`
  job widens it, to `security-events: write`, so it can upload to the Security tab. `release.yml`
  holds `contents: write` because publishing a Release needs it.
- **`main` is protected by [two rulesets](#the-two-rulesets)**, and nobody can bypass the one that
  requires the checks.

### Secret scanning

Secret scanning, push protection and validity checks are on. Push protection is the part that
blocks: it rejects a push containing a recognised secret before CI runs (see
[what each rejection means](#what-each-rejection-means)). Validity checks ask the issuing service
whether a detected token still works, so each alert in the Security tab says whether it is
**active**, **inactive** or **unknown**. An active one means rotate first, clean up second.

### Deliberately not in place

Each of these was considered and left off on purpose. Turning one on is a decision, not a fix.

- **CodeQL default setup.** It is built around pull requests, which this repository does not use,
  and it conflicts with the CodeQL job in `ci.yml`: GitHub does not accept results from both. Leave
  it at `not-configured`.
- **Dependabot version updates** (there is no `.github/dependabot.yml`). They arrive as pull
  requests, and the action pins are updated by hand instead.
- **A dependency vulnerability check in CI.** The repository has no third-party dependencies, so
  there would be nothing to scan.
- **A linter.** It would have to be installed with pip, which the zero-dependency rule forbids.
  CodeQL's quality queries cover this instead, as warnings.
- **Secret scanning's non-provider patterns and AI detection.** They mostly find false positives,
  and with one maintainer every alert is yours to triage.

### Confirming the settings

```bash
gh api repos/telus-digital/spectra --jq '.security_and_analysis'
gh api repos/telus-digital/spectra/private-vulnerability-reporting --jq .enabled
gh api repos/telus-digital/spectra/code-scanning/default-setup --jq .state   # must be not-configured
gh api 'repos/telus-digital/spectra/code-scanning/alerts?state=open' --jq length
```

## Why there are no pull requests

This repository has a single owner and maintainer, and Issues and Discussions are disabled. A pull
request would be self-approval theatre: one person opening a review for themselves to approve.

The useful half of the PR workflow is not the review, it is **required status checks** — and those
are a separate rule that works fine on a direct push. So the gate is status checks, and there are no
PRs. Dropping the review while keeping the tests is the whole design.

## The mechanism

The thing that makes this work: **check runs attach to a commit SHA, not to a branch.**

So a commit can earn its checks somewhere harmless and carry them to `main`:

1. `ship.py` force-pushes your commit to the **`ci`** branch.
2. `.github/workflows/ci.yml` triggers on that branch and runs the four required jobs.
3. Each job attaches a check run to **that SHA**.
4. `ship.py` waits for all four to complete, and stops if any failed.
5. `ship.py` pushes **the same SHA** to `main`.
6. The ruleset evaluates the pushed commit, finds four green required checks, and allows it.

`ci` is scratch space. It is force-pushed on every ship and nothing ever branches from it.

## The two rulesets

| Ruleset | Rules | Who can bypass | What it stops |
| --- | --- | --- | --- |
| **Protect main — structure** | `deletion`, `non_fast_forward` | `@alibahaloo` (always) | Accidental deletion and accidental force-push. Deliberate history rewrites stay possible. |
| **Protect main — tested** | `required_status_checks` ×4 | **nobody** | Untested and failing code. This is the real gate. |

They are split because bypass is per-ruleset, not per-rule. A single ruleset would force a choice
between keeping admin powers and having a gate. Split, you keep every admin power **except** the
power to land untested code.

There is deliberately no `pull_request` rule. It was removed when the gate moved to status checks —
left in place it fired a bypassed violation on every push, which trains you to ignore bypass
warnings. Now every bypass warning means something.

## The four required checks

```
CLI installs and runs (3.9)
CLI installs and runs (3.12)
Catalog and package stay in sync
CodeQL finds no high-severity issues
```

These strings are GitHub job names, and the ruleset matches them **literally**. The committed copy
lives in [`.github/required-checks.json`](.github/required-checks.json), and two things keep it
honest:

- [`tests/test_ci_contract.py`](tests/test_ci_contract.py) fails if `ci.yml`'s job names (matrix
  expansion included) stop matching that file.
- `ship.py` compares that file against the **live** ruleset before every push, and refuses on a
  mismatch.

The `Catalog and package stay in sync` job runs [`tools/checks.py`](tools/checks.py), which defines
the catalog-drift checks once so CI and `ship.py`'s pre-flight run the same code. Adding a check
means registering it there *and* adding a step to `ci.yml`; the contract test fails if you do only
one.

### The CodeQL check

`CodeQL finds no high-severity issues` scans the Python and the workflow files with the
`security-and-quality` query suite. CodeQL's analyze step passes whatever it finds, so the job's last
step, [`tools/codeql_gate.py`](tools/codeql_gate.py), reads the results and fails on any finding
GitHub rates **high or critical** (security-severity 7.0 or above). Everything below that, including
every quality finding, shows up as a warning on the run and in the Security tab, and never blocks.

There is no local equivalent: `--dry-run` cannot run CodeQL, so a finding first shows up when
`ship.py` waits on `ci`. Dismissing the alert in the Security tab does **not** unblock it, because the
gate reads the scan, not the alert. For a false positive, either add a CodeQL suppression comment on
the line or exclude the query in the job's `init` step, and say why in the commit. One query is
excluded today, `py/import-and-import-from`: `import unittest` beside `from unittest import mock` is
the house style in `tests/`, not a defect.

A finding you dismiss in the Security tab still appears as a warning in the job's log, for the same
reason. That is harmless: it does not block.

## What each rejection means

You will meet these as `remote:` lines on a rejected push.

| Message | What happened | What to do |
| --- | --- | --- |
| `4 of 4 required status checks are expected` | The commit has never been through CI. | Use `python tools/ship.py`. |
| `Required status check "X" is failing` | CI ran and X failed. | Read the run, fix, ship again. |
| `N of 4 required status checks are in progress` | A run is in flight — **possibly on a different commit**, see below. | Wait for it to finish. `ship.py` already does. |
| `GH013: Repository rule violations found` … `Push cannot contain secrets` | Push protection found a secret in a commit. It fires on the push to `ci`, before any CI runs. | Remove the secret from history and rotate it. Use the bypass link only for a confirmed false positive. |
| `Cannot force-push to this branch` | The structure ruleset. You have bypass, so you will see this as a *bypassed* violation on a force-push, not a rejection. | Nothing — it is informational. |

A push that succeeds but prints `Bypassed rule violations for refs/heads/main` is telling you a rule
*would* have stopped you. Read it. It should never mention status checks.

## This was measured, not assumed

Verified on 2026-09-20 against a throwaway ruleset on a throwaway branch, since deleted:

| Test | Result |
| --- | --- |
| Green SHA, checks earned on a **different** branch | **accepted** — check runs follow the SHA |
| Red SHA (deliberate catalog desync) | **rejected** — named the failing check |
| Never-tested SHA (×3 attempts) | **rejected** — `3 of 3 required status checks are expected` |

So the gate enforces *"CI ran and passed"*, not merely *"CI is not currently red"*.

Re-confirmed on 2026-09-21 against the real rulesets on `main` itself, after they were split:

| Test | Result |
| --- | --- |
| Untested commit, direct `git push origin HEAD:main` | **rejected** — `3 of 3 required status checks are expected` |
| The same commit under break glass | **accepted**, then bypass revoked |
| A second untested commit, after revoking | **rejected** again — the gate closed cleanly |
| `tools/ship.py` on a real change | **landed**, and the bypass report named no status check |

## Known edge cases

### The rename deadlock

Rename a CI job and the ruleset keeps requiring the old context, which will never appear again —
`main` becomes unpushable, and the fix cannot be delivered by a push. `test_ci_contract.py` and
`ship.py` both guard this, but if you are deliberately renaming a job, the order matters:

1. Change `ci.yml` on the `ci` branch and push it there.
2. Read the new context names off that run.
3. Update the ruleset's required contexts in the GitHub UI or via `gh api`.
4. Update `.github/required-checks.json` to match.
5. Ship normally.

### In-flight runs are counted, whoever they belong to

**The gate evaluates runs that are in flight on the branch, not only the check runs attached to the
commit you are pushing.** Observed twice:

- 2026-09-20: an untested commit was *accepted* moments after an in-flight run for a **different**
  SHA went green. The run on the accepted commit was created one second *after* the push, so it
  genuinely had no checks of its own at evaluation time.
- 2026-09-21: a push of a commit with **all three checks already green** was *rejected* with
  `2 of 3 required status checks are in progress`, because an unrelated run was still going.

So an in-flight run can both wrongly satisfy the gate and wrongly block it. Neither is something you
can reason your way around in the moment; the rule is simply: **never push to `main` while a run is
in flight.** `ship.py` waits for completion rather than for green-so-far, which is why it is the
sanctioned path. If you are pushing by hand under break glass, check first:

```bash
gh run list --branch main --limit 1
```

### Spec Kit's auto-commit hooks cannot bypass the gate

`auto_execute_hooks: true` in [`.specify/extensions.yml`](.specify/extensions.yml), and
`speckit.git.commit` runs before and after nearly every Spec Kit command. Those hooks **commit
locally only** — `git push` appears nowhere in `.claude/skills/`, `.specify/extensions/git/`, or
`.kiro/`. An agent running the Spec Kit workflow cannot put anything on `main` behind your back.

---

# Part 2 — Shipping a change

## Before you start

- On `main`, working tree clean. `ship.py` refuses otherwise, because it pushes `HEAD` and not your
  uncommitted work.
- `gh` authenticated — `ship.py` uses it to read the ruleset and poll check runs.
- Spec-driven work also needs its own branch, merged to `main` before shipping. That is a *separate*
  obligation from this gate; see the constitution's Version Control & Branching Strategy. Both apply.

Run `python tools/ship.py --dry-run` as often as you like while working. It runs the catalog checks
and the full test suite, pushes nothing, and does not mind a dirty tree.

## Path A — an agent (catalog channel)

Authoring is [`CONTRIBUTING.md` → Add a new command](CONTRIBUTING.md#add-a-new-command-use-the-spec-kit-workflow).
Once the command file exists, Principle V requires all of this **in the same change**:

1. Register the agent in [`agents-list.json`](agents-list.json) — the single source of truth for the
   roster.
2. Register the command in `spectra/extension.yml`, and any template under `provides.templates`.
3. Bump `extension.version` in `spectra/extension.yml`, with a matching `spectra/CHANGELOG.md` entry.
   Renaming or removing a command is MAJOR.
4. Mirror the version into `catalog.json`, along with `updated_at` and the command count.
5. Update `docs/index.html` so the landing page lists the command. Do **not** put a version or the
   extension description there — the page fetches both at load time, and the checks enforce it.
6. `python tools/build_package.py` — rebuild `docs/packages/spectra.zip`. Required whenever *any*
   file under `spectra/` changes, including `TRADEMARK.md` and `CHANGELOG.md`.
7. `python tools/generate_agent_docs.py` — regenerate the structured listings.
8. Hand-write the prose block a newly shipped agent needs in `AGENTS_LIST.md`.

Then:

```bash
python tools/ship.py
```

No tag and no GitHub Release: the catalog channel is **never** tagged (Principle VI). Merging to
`main` *is* its release — the raw `catalog.json` and zip URLs are live the moment the push lands.

## Path B — the CLI (CLI channel)

The ordering here is the whole point: **ship first, tag second.** The tag has to point at a commit
that already carries green checks, so tagging before shipping tags something that may never land.

1. Bump the root [`VERSION`](VERSION) file in the same commit as the code change it describes.
   MAJOR for a breaking change to the install flow, the command surface, or the prerequisites.
2. ```bash
   python tools/ship.py
   ```
3. Tag the commit that just landed, and push the tag:
   ```bash
   git tag 6.3.0 && git push origin 6.3.0
   ```
4. `release.yml` verifies the tag matches `VERSION`, then publishes "Spectra CLI 6.3.0" with
   auto-generated notes, explicitly marked **Latest**. Watch it with `gh run watch`.
5. Verify the Latest slot:
   ```bash
   gh api repos/telus-digital/spectra/releases/latest --jq '{tag: .tag_name, name: .name}'
   ```

   > **Never publish or re-publish an old release without re-checking this.** Left to GitHub's
   > default, "Latest" resolves by `created_at` with `published_at` as the tie-breaker, so touching
   > an older release can steal the slot and point `spectra update` and the landing page's version
   > pill at an ancient version. Fix with
   > `gh release edit <newest-tag> -R telus-digital/spectra --latest`.

6. Smoke-test what a consumer gets, from any directory:
   ```bash
   uv tool install spectra-cli --from git+https://github.com/telus-digital/spectra --force
   spectra
   ```
   The banner's `cli vX.Y.Z` line is the version and works anywhere. `spectra version` is
   deliberately not used here: it reports the whole stack and so needs a Spec Kit project with
   Spectra installed, which a bare smoke test has no reason to build. For a full clean-room run,
   use [`test/run.sh`](test/run.sh).

Bumping the extension does **not** bump the CLI, and vice versa. The two channels are versioned
independently and are not expected to match (Principle VI).

## Path C — everything else

Docs, specs, tooling, housekeeping. No version bump, nothing to rebuild — unless you touched a file
under `spectra/`, in which case you are on Path A whether it felt like it or not, because the zip
check will fail.

```bash
python tools/ship.py
```

## What `ship.py` does

So you can tell where it stopped:

1. Refuses a dirty tree, or a `HEAD` that is not on `main`. (Skipped for `--dry-run`.)
2. Reads the live ruleset and compares it to `.github/required-checks.json`.
3. Runs `tools/checks.py --all`, then the full test suite. `--dry-run` stops here.
4. Force-pushes `HEAD` to `ci`.
5. Polls until every required check **completes** on that SHA, then asserts they all succeeded.
6. Pushes the same SHA to `main`.

## When `ship.py` stops

| It says | Cause | Fix |
| --- | --- | --- |
| `the working tree is dirty` | Uncommitted work. `ship.py` pushes `HEAD`, not your tree. | Commit or stash. |
| `HEAD is on 'x', not main` | You are on a feature branch. | Merge or rebase onto `main` first. |
| `required-checks.json and the live ruleset disagree` | Someone renamed a job or edited the ruleset. | See [the rename deadlock](#the-rename-deadlock). Do not "fix" it by editing the JSON to match a broken ruleset. |
| a check failed in the pre-flight | Real drift, caught locally. | The message names the file and the command that fixes it. |
| `the test suite failed` | Real breakage. | Nothing was pushed. |
| `... never started on <sha>` | The `ci` branch is no longer in `ci.yml`'s push trigger. | Restore `branches: [main, ci]`. |
| `required check(s) failed` | CI ran and failed on the real runner. | `gh run list --branch ci --limit 1`, read it, fix, ship again. |
| `no ruleset requires status checks yet` | Informational, not an error. The gate is not configured. | Only expected before the ruleset exists. |

---

# Part 3 — Break glass

If GitHub Actions is down or wedged, nothing can earn checks and `main` is unpushable. That is the
gate working as designed, and it has a deliberate, manual escape. It is manual on purpose: a
scripted `--break-glass` flag would be a one-flag hole in the thing the gate exists to prevent.

Find the ruleset:

```bash
RULESET=$(gh api repos/telus-digital/spectra/rulesets --jq '.[] | select(.name | contains("tested")) | .id')
```

Grant yourself bypass:

```bash
gh api -X PUT repos/telus-digital/spectra/rulesets/$RULESET --input - <<'JSON'
{"bypass_actors": [{"actor_id": 4724492, "actor_type": "User", "bypass_mode": "always"}]}
JSON
```

Push what you must, then **revoke it immediately**:

```bash
gh api -X PUT repos/telus-digital/spectra/rulesets/$RULESET --input - <<'JSON'
{"bypass_actors": []}
JSON
```

Confirm it is closed again:

```bash
gh api repos/telus-digital/spectra/rulesets/$RULESET --jq '{bypass: .bypass_actors, can_bypass: .current_user_can_bypass}'
```

It should print `{"bypass":[],"can_bypass":"never"}`.

The ruleset's own history is the audit trail — every grant and revoke is recorded, which is most of
why this is worth doing by hand rather than hiding it in a script. When you use it, ship the proper
fix through the normal path as soon as Actions is back.
