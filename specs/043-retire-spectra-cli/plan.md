# Implementation Plan: Retire the spectra CLI

**Branch**: `043-retire-spectra-cli` | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/043-retire-spectra-cli/spec.md`

## Summary

Delete the `spectra` CLI and everything that exists only for it, leaving the `spectra` extension as the
only thing SPECTRA ships. Two small pieces of CLI code that maintainer tooling still uses (the roster
parser and the manifest-version scanner) move into `tools/`. The two required CI checks that install the
CLI are replaced by one required check that runs the test suite without installing anything, switched over
with `SHIPPING.md`'s rename procedure. The governing documents describe one release channel (the
constitution is already amended to 3.0.0 on this branch), and every install, update, and positioning text in
the README and `docs/` is rewritten around `specify` commands, verified against Spec Kit 1.4.5. Research
confirmed that Spec Kit 1.4.5 registers an extension only for the default integration and that an update
strips it from the others, so the docs carry the `specify integration use` rotation. After the merge, the
maintainer deletes the 13 CLI Releases and tags.

## Technical Context

**Language/Version**: Python 3 standard library only (maintainer tooling and tests); HTML/CSS/JS (static
`docs/` pages); Markdown and YAML (extension, governing docs). No Python version floor is enforced after
this change (FR-009); CI runs the current stable Python.

**Primary Dependencies**: None. The zero-third-party-dependency rule holds for everything that remains
(FR-004). External tools are used, not depended on: Spec Kit's `specify` CLI 1.4.5 (the baseline, FR-029)
for verification, and `gh` for the maintainer's ruleset and Release steps.

**Storage**: Files in the repository. Published artifacts stay at their paths: `catalog.json`,
`docs/packages/spectra.zip`, `agents-list.json` (FR-006).

**Testing**: `python3 -m unittest discover -s tests`; `python3 tools/checks.py --all`;
`python3 tools/generate_agent_docs.py --check`; a manual clean-room install in a scratch Spec Kit project
on 1.4.5 (see [quickstart.md](quickstart.md)).

**Target Platform**: GitHub (repository, Actions, rulesets, Pages serving `main` `/docs`); users' machines
running Spec Kit on macOS, Windows, or Linux.

**Project Type**: Spec Kit extension repository (Markdown/YAML payload) with maintainer tooling and a static
documentation site.

**Performance Goals**: N/A.

**Constraints**: `main` must accept a correctly tested push at every point (FR-011); nothing under
`spectra/` changes (FR-005); historical records stay as written (FR-025); the maintainer, not the
implementation run, changes the live ruleset and deletes Releases and tags (FR-011, FR-030).

**Scale/Scope**: About 4,800 lines of CLI Python and 14 CLI-only test modules removed; 2 parsers moved; 5
test modules and the shared helpers repointed; 1 CI job replaced; 5 governing documents and the README updated; 18 `docs/`
pages edited (6 with substantial rewrites).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against constitution **3.0.0** (amended on this branch for this feature).

| Principle | Gate | Status |
|---|---|---|
| I. Spec-Driven Development | Feature work goes through specify → plan → tasks → implement, each user-invoked | ✅ Spec, clarify and this plan were each invoked by the user; tasks and implement follow the same way |
| II. Single self-contained extension | One `spectra/` extension, no new extension folders | ✅ `spectra/` is untouched |
| III. Agent-agnostic commands | Commands in generic format, `speckit.spectra.*` | ✅ No command changes |
| IV. Context-aware by default | Commands read real project context | ✅ No command changes |
| V. Catalog and package in sync | `agents/` is the only source of agent facts; generated outputs not hand-edited; published pages read version and description from `catalog.json`, roster from `agents-list.json` | ✅ No agent change, so no extension bump or zip rebuild. The footer on `docs/getting-started/agents.html` sits outside the generated regions. The landing page keeps the `catalog.json` version badge and loses the Release badge. The roster parser moves with its behaviour unchanged, so the generator still validates `agents-list.json` the same way |
| VI. A single release channel | One channel; merging to `main` is the release; no git tags, no GitHub Releases | ✅ This feature is what makes the repository conform: `release.yml` removed and Releases and tags deleted by the maintainer after merge (FR-030) |
| VII. Document artifacts under one root | Applies to commands that write deliverables | ✅ N/A, no command changes |
| VIII. Overridable templates | Applies to document-producing commands | ✅ N/A, no template changes |
| Publishing standards | SemVer for the extension; no silent drift between `catalog.json`, zip, landing page, agents page | ✅ Extension version unchanged; `tools/checks.py` still enforces parity |
| Development workflow | Test locally with `specify extension add`; publish via `tools/ship.py` | ✅ The quickstart verifies the published path on 1.4.5; landing follows `SHIPPING.md` |
| Version control & branching | One branch per spec, named after it; nothing reaches `main` without green required checks | ✅ Branch `043-retire-spectra-cli`. The required-check switch follows the rename procedure ([contracts/required-checks.md](contracts/required-checks.md)); break-glass is not used |
| Governance: amendment procedure | Dependent docs updated in the same change as the amendment | ✅ The 3.0.0 amendment and the dependent-doc updates land on `main` in the same merge of this branch. The Sync Impact Report comment is removed before commit |

**Pre-research result**: PASS, no violations.

**Post-design re-check**: PASS. The design adds no new top-level folders, no dependencies, no generated
outputs, and no published data typed into HTML. The one new rule the design leans on, "no tags, no Releases",
is now satisfied by construction rather than by convention.

## Project Structure

### Documentation (this feature)

```text
specs/043-retire-spectra-cli/
├── spec.md
├── plan.md                      # This file
├── research.md                  # Phase 0: decisions and the Spec Kit 1.4.5 findings
├── data-model.md                # Phase 1: file disposition and the entities the docs rely on
├── quickstart.md                # Phase 1: how to prove the feature works end to end
├── contracts/
│   ├── install-commands.md      # The canonical specify command set every doc must use
│   ├── required-checks.md       # The new required-check contract and the switch sequence
│   └── positioning.md           # Product description, footer tagline, banned phrases
├── checklists/
│   └── requirements.md
└── tasks.md                     # Phase 2 (/speckit-tasks, not created here)
```

### Source Code (repository root)

```text
spectra/                         # UNCHANGED: the extension
agents/                          # UNCHANGED: agent source of truth
catalog.json                     # UNCHANGED
agents-list.json                 # UNCHANGED (generated)
docs/packages/spectra.zip        # UNCHANGED

spectra_cli/                     # DELETED
pyproject.toml                   # DELETED
VERSION                          # DELETED
test/                            # DELETED (Docker clean-room harness)
.github/workflows/release.yml    # DELETED

.github/workflows/ci.yml         # `cli` job replaced by `tests` ("Tests pass")
.github/required-checks.json     # new context list
.gitignore                       # drop the pip build-artifact block

tools/
├── roster.py                    # NEW: roster parser moved from spectra_cli/roster.py (no network code)
├── checks.py                    # owns parse_manifest_version (moved from spectra_cli/extension.py)
├── generate_agent_docs.py       # imports tools/roster.py
├── build_package.py, codeql_gate.py, ship.py, agent_source.py, markdown_subset.py
│                                # docstrings no longer cite pyproject.toml / the CLI
└── ...

tests/
├── test_roster.py               # repointed to tools/roster.py; fetch/network cases dropped
├── test_roster_data.py          # repointed; manifest-version assertion via tools/checks.py
├── test_generator.py            # repointed
├── test_ci_contract.py          # repointed; matrix-less job supported
├── test_codeql_gate.py          # sample paths no longer name spectra_cli/
├── helpers.py                   # CLI-only fixtures pruned; docstring updated
├── test_manifest_version.py     # NEW: the manifest-version cases kept from test_extension.py
└── (14 CLI-only modules)        # DELETED, see data-model.md

.specify/memory/constitution.md  # 3.0.0 (already amended on this branch)
CLAUDE.md, CONTRIBUTING.md, SECURITY.md, SHIPPING.md, README.md
docs/index.html, docs/capability-brief.html, docs/getting-started/index.html,
docs/getting-started/spectra.html, docs/getting-started/agents.html (footer only), docs/agents.html,
docs/e-learning/*.html
```

**Structure Decision**: No new top-level folders. Maintainer logic that outlives the CLI moves into the
existing `tools/` directory, which is where every other piece of maintainer tooling lives and which never
ships. `tools/roster.py` becomes the single roster parser, keeping the "one parser" property the generator
relies on. The manifest-version scanner moves into `tools/checks.py`, its only remaining caller. Full
per-file disposition is in [data-model.md](data-model.md).

## Delivery sequence

The order matters because of the gate on `main` and the governance rule that the amendment lands with its
dependent changes.

1. **On the branch**: remove the CLI, move the parsers, repoint and prune the tests, replace the CI job and
   `required-checks.json`, and update the governing docs, README and `docs/`. Remove the Sync Impact Report
   comment from the constitution. All local checks pass (`unittest`, `checks.py --all`,
   `generate_agent_docs.py --check`).
2. **Verify the published install path** in a scratch project on Spec Kit 1.4.5, following the rewritten
   landing page exactly ([quickstart.md](quickstart.md), Scenarios 1 to 3).
3. **Merge the branch into `main` locally** (constitution: spec work merges back when complete).
4. **Rename procedure** ([contracts/required-checks.md](contracts/required-checks.md)): push the merged SHA
   to `ci` and read the new contexts off that run. The **maintainer** switches the live ruleset to them, and
   then `python3 tools/ship.py` lands the SHA on `main`.
5. **Maintainer deletes the 13 Releases and tags** (FR-030) and confirms none remain.
6. The maintainer tells internal users to uninstall the CLI. This is outside the feature.

## Complexity Tracking

No constitution violations to justify.
