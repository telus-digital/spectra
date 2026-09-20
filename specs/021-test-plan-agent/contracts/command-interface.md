# Contract: Command Interface

**Command**: `speckit.spectra.test-plan` | **File**: `spectra/commands/test-plan.md` | **Effect**: `read-write`

## Identity

| Property | Value |
|---|---|
| Name | `speckit.spectra.test-plan` |
| Registered in | `spectra/extension.yml` → `provides.commands` |
| Front matter | YAML with a `description` (Principle III) |
| Input mechanism | `$ARGUMENTS`, agent-agnostic |
| Runtime tool requirements | **none** — no `git`, no `gh`, no network |
| Writes | exactly one file per run |

## The argument

**Required.** One path, after any flags are removed.

| Input | Behaviour |
|---|---|
| empty | Ask for a specification path. **Stop.** Read nothing, analyze nothing, write nothing |
| a readable specification file | Resolve directly |
| a directory containing exactly one `spec.md` | Resolve to it, and say so |
| a directory with no `spec.md` | Report the directory. **Stop** |
| a directory with several candidates and no `spec.md` | List what was found, ask. **Do not choose** |
| a missing or unreadable path | Report the path and the reason. **Stop** |
| a readable file that is not usable as a specification | Report why. **Stop** |
| a path resolving outside the invoking project | Report the conflict. **Stop before writing** |

**Usability**, deliberately weak: Markdown-like text, non-empty, at least one heading, and at least one of
a requirements, user-scenario, acceptance-criteria, or success-criteria section under any wording. The
Spec Kit template's exact headings are **not** required — a project may override its spec template.

### The inference prohibition

With an empty argument the command MUST NOT consult, in any form:

- the current Git branch name
- `.specify/feature.json` or any other feature record
- file modification times
- the contents or listing of `specs/`
- a prior run, a cache, or session history

This is the one place where the command is deliberately less helpful than the rest of the workflow. The
reason belongs in the command text, so a future editor reads it before removing it: the output is
circulated and approved, and a plan generated against the wrong specification is undetectably wrong to
whoever signs it.

## Flags

| Flag | Effect |
|---|---|
| `--non-interactive` | Declare up front that no answer can be taken. Creates a plan that does not exist; never rewrites one |

No other flag is defined. An unrecognized flag is reported and ignored; it never silently becomes part of
the path.

## What the command never does

Absolute. No argument, attachment, or instruction anywhere in the session enables any of them.

| Never | Why |
|---|---|
| Infer which specification was meant | The output gets signed. See above |
| Write more than one file | One test plan per run, and nothing else |
| Modify the specification it read | It may be under review; a Spectra-specific edit invalidates that review |
| Write, modify, or generate test code | The plan says what will be verified; `/speckit-implement` writes it |
| Modify test framework, coverage, or CI configuration | It recommends; the team applies |
| Run, build, or install anything — including the test suite | Existing coverage is read, never executed |
| Make a network request, or accept a repository URL, credential, or token | It reads only the project in front of it |
| Edit the constitution, create a branch, stage, or commit | Producing a document is not a licence to edit governance or history |
| Edit a core Spec Kit command, or register a hook | `/speckit-specify` and `/speckit-plan` stay unaware of this agent |
| Invoke another command | It prints the invocation; the user runs it |
| Create or edit a template file | Templates are input |
| Reproduce a secret value, whole or partial | Name the kind and where it is configured; withhold the value |
| Emit a checkbox, in any section, from any template layer | This is an approval document, not a tracker |
| Write a claim of absence with no search behind it | "Not found in what was searched" is permitted; "not covered" unqualified is not |

## Write scope

```text
<resolved spec's directory>/test-plan.md      ← the only file, ever
```

No artifact root is resolved for output. No subfolder is created. No sequence number is assigned. No
index, no cache, no state under `.specify/`.

The declared artifact root **is** resolved, read-only, for one purpose: locating
`<artifact-root>/test-strategy/TEST_STRATEGY.md`. No publication check is performed, no `documents/`
fallback is recommended, and the declaration line is never offered — none of those obligations attach to
reading.

## Effect classification

`read-write`, matching the manifest. The write is one Markdown file inside the project, gated on
confirmation when it would replace an existing one.
