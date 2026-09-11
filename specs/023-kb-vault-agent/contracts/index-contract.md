# Contract — The Category Index

## Status: a directory listing, not an artifact

`<artifact-root>/<category>/README.md` holds no field that is not derivable from the documents in the
folder. It is navigation over one artifact type, rebuilt from what is present — which is why it does
not violate Principle VII's one-artifact-type-per-folder rule. The argument is made at length in
`specs/022-defect-rca-agent/plan.md`; this contract adds only what is specific to kb-vault.

## Where it exists, and where it must not

| Folder | Index |
|---|---|
| A category folder kb-vault owns | Maintained |
| A reserved-map folder — `adr/`, `brd/`, `impact-analysis/`, `test-strategy/`, `defect-rca/` | **Never introduced.** Those agents' conventions are not kb-vault's to change |
| A folder where the project already keeps an index | **Updated, never replaced.** A hand-maintained index may carry columns a rebuild cannot know about |
| The artifact root itself | Never. An index across categories is a second file type at the root level |

## Shape

```markdown
# <Category title>

<!-- Rebuilt by speckit.spectra.kb-vault. Rows follow the documents in this folder. -->

| Document | Subject | Ingested |
|---|---|---|
| [001-branching-and-release.md](001-branching-and-release.md) | Branching model, review expectations, release train | 2026-09-11 |
| [002-incident-severities.md](002-incident-severities.md) | Severity definitions and escalation paths | 2026-09-11 |
```

## Column rules

| Column | Rule |
|---|---|
| Document | Relative link to the file in this folder. Never an absolute path. |
| Subject | What the document is about, one line. The same judgement the plan table's description carried. |
| Ingested | The run date the document was created or last updated by kb-vault. |

Where the project's existing index carries other columns, those columns are preserved and the new row
is filled as far as it can be.

## Invariants

- **Rebuilt from the folder.** A hand-added file gains a row on the next run; a hand-deleted file loses
  one. The index never asserts a document that is not there.
- **One folder, one index.** It lists the documents in its own folder and no others.
- **It is not a source.** Duplicate detection may read it as shortlist metadata, but a match is
  confirmed against the documents themselves.
- **It is written under the same gate.** An index update is part of the approved write, not a side
  effect that happens regardless.
