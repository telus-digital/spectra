# Data Model: One-Step Remedy When the Folder Is Not a Spec Kit Project

No persisted data. The only "model" is the set of project states the CLI distinguishes, each with its
own message and remedy. Only the first row changes.

| State | Detected when | Message (first line) | Remedy line(s) | Exit code |
| --- | --- | --- | --- | --- |
| Not a Spec Kit project | no `.specify/` in cwd or any parent | `✗ This is not a Spec Kit project — …` | **new:** `  Initialize Specify and add Spectra: spectra install` (was two lines) | `EXIT_PROJECT_STATE` (unchanged) |
| Spec Kit, no Spectra | `.specify/` found, Spectra not installed | `! Spectra is not installed in this project (…)` | `  Install it with: spectra install` | unchanged |
| Incomplete install | Spectra partially present | unchanged | unchanged | unchanged |
| Installed | Spectra present | unchanged | — | `EXIT_OK` |

**Invariant**: each state keeps a distinct first sentence (the existing SC-009 test in
`tests/test_check.py` depends on this).
