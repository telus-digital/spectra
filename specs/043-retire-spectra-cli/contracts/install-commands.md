# Contract: the `specify` commands the docs use

Every install, keep-current, multi-agent, and remove instruction in `README.md`, `docs/index.html`,
`docs/getting-started/index.html`, and `docs/e-learning/*.html` uses these commands, spelled exactly as
below. Verified on Spec Kit **1.4.5** ([research.md](../research.md) R2, R3). A page may show a subset, but
it may not introduce a different command for the same job.

## Install (FR-019: the one path)

Prerequisites: uv and Git (OS-specific check and install steps stay as they are on the landing page), and
internet access to `github.com` and `raw.githubusercontent.com`.

```bash
# 1. Install Spec Kit (once per machine)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 2. Initialize a Spec Kit project (skip if the folder already has .specify/)
specify init --here

# 3. Register the SPECTRA catalog (once per project; commit .specify/extension-catalogs.yml)
specify extension catalog add https://raw.githubusercontent.com/telus-digital/spectra/main/catalog.json --name spectra --priority 5 --install-allowed

# 4. Install SPECTRA, then restart your coding agent
specify extension add spectra
```

Required notes alongside the steps:
- `--install-allowed` is required, because catalogs are discovery-only by default.
- Committing `.specify/extension-catalogs.yml` lets everyone who clones the project inherit the catalog.
- Restart the agent so it picks up the new commands, then see the agent reference.

## Keep current (FR-019, User Story 3)

```bash
specify self check                 # is a newer Spec Kit available?
specify self upgrade               # upgrade Spec Kit
specify integration upgrade        # bring the project's core agent files current
specify extension update spectra   # update SPECTRA (asks to confirm)
specify extension list             # what is installed, and at which version
```

## Projects with more than one agent (FR-028, verified behaviour)

Statement the docs must make, in substance:

> Spec Kit registers an extension's commands only for the project's **default** agent, and an update that
> installs a newer version of SPECTRA removes them from every other agent. If your project has more than
> one agent installed, give the others SPECTRA's commands by making each one the default briefly, then
> setting your usual default back. Do this after installing SPECTRA, and again after any update that
> installed a newer version.

```bash
specify integration status            # lists installed agents and the current default
specify integration use <other-agent> # registers SPECTRA's commands for that agent
specify integration use <your-default># sets your default back (it keeps its commands)
```

## Remove (FR-019)

```bash
specify extension remove spectra
```

It removes SPECTRA's commands from every agent in the project and leaves Spec Kit, other extensions, and
the default agent untouched.

## Forbidden in current docs (FR-025, FR-026)

Any `spectra` CLI invocation (`spectra`, `spectra install|check|version|update|uninstall|agent-list`,
`spectra cli …`), `uv tool install spectra-cli …`, `uv tool uninstall spectra-cli`, `--no-update-check`,
`SPECTRA_NO_UPDATE_CHECK`, and any guidance for people who still have the `spectra` command.
