# Contract — The Plan Table and the Approval Gate

The table is the whole safety mechanism. It is a faithful statement of what the run will do: every row
is achievable within the write scope, and no row appears that the command would later refuse (R11).

## Shape

```markdown
| Doc category | Doc description | Doc location | Action |
|---|---|---|---|
| `adr` | The 2024 decision to move order processing onto a queue, with the alternatives weighed at the time | `docs/adr/ADR-007-queue-based-order-processing.md` | Create (folder exists) |
| `ux-ui-standards` | Component spacing, type scale and colour tokens for the design system | `docs/ux-ui-standards/002-component-spacing-and-type.md` | Update — `docs/ux-ui-standards/002-component-spacing-and-type.md` |
| `engineering-methodology` | Branching model, review expectations and the release train | `docs/engineering-methodology/001-branching-and-release.md` | Create (folder will be created) |
```

The first three columns are the ones the request names. `Action` is the fourth because the request's
own "update it, not add a new file of the same nature" is invisible without it.

## Column rules

| Column | Rule |
|---|---|
| Doc category | The Documentation Category slug, in backticks. Derived from content, never filename. |
| Doc description | What the document will contain, in one line, from the source's content. Not the source's filename, not a category definition. |
| Doc location | Project-relative path **including the filename**. Lowercase. Never absolute. |
| Action | `Create (folder exists)`, `Create (folder will be created)`, or `Update — <existing path>`. |

## Beneath the table

Listed only where they apply. Each is a sentence, not a section:

- Sources that could not be read, by name, with what is needed from the user.
- Sources merged into one row, and which row.
- One source producing several rows, and which.
- A contradiction between a source and the document a row would update.
- A conflict between a source and the constitution.
- A superseded folder found, named once, with the note that it is left alone.
- An existing document the command judged a match — stated as a judgement, so it can be corrected.
- The `Artifact root:` line, where the root is not declared.

## The gate

After the table and its notes, in the command's own voice:

1. An explicit statement that **nothing has been written yet**.
2. A single question asking for approval.
3. A stop.

## Rules of the gate

- **Approval is affirmative.** A question, a comment, a partial reaction, or an ambiguous response is
  not approval. Where it is unclear, nothing is written and the command says so.
- **Any change re-enters the gate.** A redirection, rename, drop, split or merge produces a full
  revised table and a fresh question — never a write on the strength of the redirection alone.
- **Re-planning does not re-read.** Correcting a row must not cost the user their attachments or
  another absorption pass.
- **A subset may be approved.** Rows not approved are not written, and are named in the report.
- **The user may change**: a row's category, its filename, its category folder, whether it is a create
  or an update, which existing file an update targets, and whether the row happens at all.
- **The user may not change**: a create's destination to somewhere outside the resolved artifact root.
  That request is answered with the two routes that reach it legitimately.
