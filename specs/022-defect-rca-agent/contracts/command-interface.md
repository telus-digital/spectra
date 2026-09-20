# Contract — Command Interface

**Command**: `speckit.spectra.defect-rca` | **File**: `spectra/commands/defect-rca.md`
**Effect**: read-write (two files, one folder) | **Feature**: `022-defect-rca-agent`

## Registration

```yaml
# spectra/extension.yml → provides.commands[]
- name: "speckit.spectra.defect-rca"
  file: "commands/defect-rca.md"
  description: "Guide a hypothesis-driven root cause analysis of a defect from a JIRA ticket, GitHub issue, or description, and write the RCA document into the project's artifact root."
```

```yaml
# spectra/extension.yml → provides.templates[]
- name: "defect-rca-template"
  file: "templates/defect-rca-template.md"
  description: "Section structure for the root cause analyses produced by speckit.spectra.defect-rca. Override at .specify/templates/overrides/defect-rca-template.md. The symptom/root-cause distinction, answer-first ordering, the recording of invalidated hypotheses, evidence-source attribution, the advisory status line, the related-prior-RCA field, and the prohibition on reproducing a secret stay with the command."
```

The command file MUST open with YAML front matter carrying a `description` (FR-002).

## Input

`$ARGUMENTS` carries the defect. Nothing else is read from the invocation.

| Input | Resolved channel | Behaviour |
|---|---|---|
| `https://github.com/<org>/<repo>/issues/42` | `github-issue` | Fetch body **and comments** via `gh`. |
| `PROJ-1234`, or a JIRA URL | `jira` | Retrieve through the host agent's existing JIRA access. |
| Free prose | `plain` | Use as given. |
| Prose plus pasted logs | `plain` | Same, with the material taken as supplementary. |
| *(empty)* | none | Ask what defect to analyze, and **stop**. |

**MUST**: state the resolved channel before gathering evidence (FR-008).
**MUST NOT**: infer a defect from the branch name, recent commits, open issues, failing tests, or any
other heuristic; read source; or write anything, when the input is empty (FR-009).

## Retrieval and degradation

| Condition | Response |
|---|---|
| `gh` absent | Say so. Remedy: install `gh`. Ask for a paste. Continue as `plain`. |
| `gh` present, not authenticated | Say so. Remedy: `gh auth login`. Ask for a paste. Continue as `plain`. |
| Issue private, deleted, or not found | Say which. Ask for a paste. Continue as `plain`. |
| No JIRA access in the host agent | Say so. Ask for a paste. Continue as `plain`. |
| JIRA reachable, ticket denied | Say so. Ask for a paste. Continue as `plain`. |

**MUST NOT**, in any of these branches: prompt for, accept, transmit or store a credential, API token
or password; attempt to authenticate on the user's behalf; or suggest the user paste a token into the
session (FR-013).

**MUST NOT**: make any outbound request other than the ticket or issue retrieval above; accept a
repository URL to clone (FR-014).

## Modes

Reached by what the user says, not by flags (D7).

| Mode | Entry | Writes |
|---|---|---|
| Intake | A defect in `$ARGUMENTS` | nothing |
| Hypothesis loop | Continues from intake | nothing |
| Synthesis | The user asks to synthesize | **document + index** |
| Issue-tree exploration | A defect *class*, no specific defect | nothing |
| Reflection | After synthesis | nothing |

Reflection requested with no analysis behind it MUST say so rather than assess (FR-037).
Exploration MUST create and modify nothing anywhere in the project (FR-035).

## Write scope

The command writes exactly two paths, both under `<artifact-root>/defect-rca/`:

1. `NNN-<slug>.md` — the analysis
2. `README.md` — the index

**MUST NOT**: write anywhere else in the repository (FR-055); generate, apply or execute a code fix,
patch or configuration change; write, modify or generate test code (FR-056); write back to JIRA or
GitHub, create an issue or comment, or transition a ticket (FR-057); edit the constitution, create a
branch, stage, or commit (FR-058).

Where an `Artifact root:` declaration would help, the command offers the exact line and lets the user
add it (FR-058).

## Completion report

Every run that writes reports, at minimum (FR-060):

- the path written;
- the template layer resolved, by path;
- the artifact root used and how it was determined — declared, default, or chosen after a publication
  signal;
- the commit analyzed;
- which prior RCAs were surfaced, and on which axis;
- what it could not examine.

## Budgets

| Budget | Default |
|---|---|
| Clarifying questions per round | 5 (D8) |
| Major hypothesis-tree branches | ≥ 5 (FR-025) |
| Issue-tree major branches | ≥ 4 (FR-035) |

The root-resolution question does not count against the question budget. Reaching a cap is a
disclosure, never a silent stop.
