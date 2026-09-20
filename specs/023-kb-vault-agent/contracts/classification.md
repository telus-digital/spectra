# Contract — Classification, the Reserved Map, and Duplicate Matching

## Deriving a category

From the **content** of the source. Never from its filename, extension, or size.

A category is a lowercase kebab-case slug that would be a valid folder name. The set is open-ended: a
supplied document of a kind nobody anticipated gets a derived slug, not a refusal and not a junk
drawer.

One source may carry several categories — a deck covering both a decision and a standard produces two
rows. Several sources may carry one — three documents about the same standard produce one row, and the
table says which three.

## The reserved map

A category that corresponds to a document type another Spectra agent already produces adopts that
agent's folder, naming and template **wholesale**:

| Source is | Folder | Filename | Template |
|---|---|---|---|
| an architecture decision | `<artifact-root>/adr/` | `ADR-NNN-<kebab-title>.md` | `adr-template` |
| a business requirements document | `<artifact-root>/brd/` | `NNN-<kebab-title>.md` | `brd-template` |
| an impact analysis | `<artifact-root>/impact-analysis/` | `NNN-<kebab-title>.md` | `impact-analysis-template` |
| a test strategy | `<artifact-root>/test-strategy/` | the project's existing name | `test-strategy-template` |
| a defect root cause analysis | `<artifact-root>/defect-rca/` | `NNN-<kebab-title>.md` | `defect-rca-template` |

In a reserved folder, kb-vault is a second author into one set — not a second set. It introduces no
index there, no alternative numbering, and no alternative shape.

Anything else: `<artifact-root>/<slug>/`, `NNN-<kebab-title>.md`, template `<slug>-template` resolved
through the stack, falling back to `kb-document-template`.

## Duplicate matching

Two staged reads, bounded by the documentation tree rather than the repository.

**Stage 1 — shortlist.** From the Repository Documentation Profile, take the candidate folders: the
category's own folder, the reserved-map folder where applicable, any superseded folder for that
category, and any documentation folder the survey found. Shortlist by filename and top-level heading.

**Stage 2 — compare.** Read the shortlist. A match is a document of the **same category** about the
**same subject**.

### The match axes

| Axis | Matches on |
|---|---|
| Category | The same kind of document. A standard does not match a decision record. |
| Subject | What it is *about* — the system, the decision, the standard — not its title. |
| Scope | A document about the whole design system matches one about the whole design system, not one about a single component. |

Title similarity alone is never a match. `standards.md` and `ux-guidelines.md` may be the same
document; `adr-005.md` and `adr-006.md` are not.

### What a match produces

An `update` row whose `target` is the matched file, whose location is that file's existing path, and
whose notes carry any contradiction between the source and the target.

### What a match is not

A match is a **judgement**, and the table says so — because the user is the one who knows. Correcting a
wrong match at the gate must cost one sentence and no re-absorption. Correcting a *missed* match — the
user points at an existing file the command did not find — converts the row from `create` to `update`
in place.

## Failure modes this contract exists to prevent

| Failure | Prevented by |
|---|---|
| A second ADR set beside the ADR agent's | The reserved map |
| Two standards documents disagreeing with each other | Stage 2 subject matching |
| An update to the wrong document | The match stated as a judgement, correctable at the gate |
| A category derived from `notes.pdf` | Derivation from content only |
| An unbounded scan of a large repository | The candidate-folder shortlist |
| A supplied deck landing as one undifferentiated file | One source → several rows |
