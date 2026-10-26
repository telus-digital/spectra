# Spectra — notes for coding agents

Read `.specify/memory/constitution.md` first — it governs how Spectra is built, and the
Constitution Check gate in every plan is binding.

**Feature work goes through specs, and the user runs every phase (Principle I).** Adding an agent,
materially changing what an agent does, changing how the `spectra` CLI works, or changing how Spectra
is packaged or released is feature work. When asked for it in plain chat, do not build it and do not
start the workflow: say it is feature work, give a ready-to-paste `/speckit.specify` prompt, and stop.
Never run `specify`, `clarify`, `checklist`, `plan`, `tasks`, `analyze`, `converge`, `taskstoissues`,
or `implement` yourself — a chat request to run one is answered with the command, not by running it.
When the user invokes one, do that one phase, summarize it, name the next command, and stop. Small bug
fixes, cosmetics, and housekeeping need no spec and can be done directly, but still follow every other
principle (version bump and package resync for a command fix, `tools/ship.py` to land).

Two independently-versioned things live in this repo. Know which one you are changing:

- **`spectra/`** — the Spec Kit extension (the agents). Markdown + YAML, no code. Versioned in
  `spectra/extension.yml`, mirrored into `catalog.json`, shipped from `main` over raw URLs. Never
  tagged. Adding or changing a command means updating `agents/<id>.md`, `extension.yml`,
  `spectra/CHANGELOG.md`, `catalog.json`, and `docs/packages/spectra.zip`, then regenerating, in the
  same change (Principle V).
- **`spectra_cli/`** — the `spectra` command that manages Spectra in a project. Python, stdlib
  only, installed as a `uv` tool. Versioned in the root `VERSION` file and released by pushing a bare
  semver git tag. Git tags and GitHub Releases belong to this channel exclusively (Principle VI).

Never bump one channel because the other moved.

## `agents/` is the source of truth

Every fact about an agent lives in `agents/<id>.md` — a flat `key: value` header (id, title, command,
provider, type, phase, order, status, summary, manifest) and, for a shipped Spectra agent, a Markdown
body holding its long description. Phases live in `agents/_phases.md`. Nothing about an agent is
written anywhere else: every listing is rendered from that source and must not be hand-edited.

| Generated output | File |
| --- | --- |
| whole file | `agents-list.json` |
| `agents-list-table`, `agents-list-shipped`, `agents-list-speckit-core`, `agents-list-roadmap` | `AGENTS_LIST.md` |
| `spectra-readme-commands`, `spectra-readme-agents` | `spectra/README.md` |
| `agents-page-nav`, `agents-page-cards` | `docs/getting-started/agents.html` |
| each command's `description:` line | `spectra/extension.yml`, `spectra/commands/<id>.md` |

```bash
python3 tools/generate_agent_docs.py            # render every output from agents/
python3 tools/generate_agent_docs.py --check    # what CI runs
python3 tools/build_package.py                  # rebuild docs/packages/spectra.zip
```

To change an agent, edit `agents/<id>.md` and run the generator. `--check` fails if any output differs
from what `agents/` renders (a stale output or a hand edit), if the source breaks the format, if
`agents/` and `spectra/extension.yml` disagree about the shipped set, or if a page names a
`speckit.spectra.*` command that `agents/` does not ship. Body Markdown is a fixed subset (no raw HTML,
no `###`); the generator refuses anything else and names the file and line.

## The command surface

A top-level verb acts on the agents in the current project; only `spectra cli …` acts on the tool.
`--version`, `--update`, and `--uninstall` were removed in CLI 5.0.0.

## Tests

Standard-library `unittest`, not pytest — the zero-dependency constraint applies to the whole
repository, not just the shipped wheel.

```bash
python -m unittest discover -s tests
```

## How changes land

**Never `git push origin main`.** `main` is gated: a branch ruleset accepts a push only when the
commit already carries green runs of every required CI check, and nobody can bypass it.

```bash
python tools/ship.py             # checks + tests, earn CI on the `ci` branch, then push main
python tools/ship.py --dry-run   # checks + tests only, pushes nothing, tolerates a dirty tree
```

Read `SHIPPING.md` before shipping anything for the first time, and whenever a push is rejected — it
explains the mechanism, what each rejection message means, the per-channel release paths, and the
break-glass procedure. Changing a CI job name without reading it will make `main` unpushable.

Contributor workflow and packaging: `CONTRIBUTING.md`. Landing a change: `SHIPPING.md`.
Per-feature design artifacts live under `specs/<NNN>-<name>/`; note that the older ones predate the
single-extension consolidation and describe a build script that no longer exists.

<!-- The block below is owned by the agent-context extension and is REPLACED WHOLESALE whenever
     `speckit.agent-context.update` runs — its script writes a fixed template rather than preserving
     what is inside the markers. Keep hand-written guidance above this line, never inside it. -->
<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/006-agent-roster-cli/plan.md
<!-- SPECKIT END -->
