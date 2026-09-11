# Phase 0 — Research: KB Vault

Eleven decisions. Each records what was chosen, why, and what was rejected. The three genuine unknowns
in the specification were resolved with the user before this plan began and are recorded in
[spec.md](./spec.md) under Clarifications; what follows is design research, not clarification.

---

## R1 — Command name, agent id, and roster placement

**Decision**: the command is `speckit.spectra.kb-vault`; the roster id is `kb-vault`; the phase is
`foundation`; `type` is `add-on`, `provider` is `spectra`, `status` is `available`. The entry is
inserted **inside the existing `foundation` block** in `agents-list.json`, immediately after
`domain-analyzer`.

**Rationale**: Spec Kit validates command names against `^speckit\.<extension-id>\.<command>$`, so
`/kb-vault` cannot be registered as typed — Principle III settles the name without discretion. The
phase is `foundation` because kb-vault establishes the documented context every later agent reads,
which is the same job `domain-analyzer` does for the domain. The insertion *position* is not cosmetic:
`tests/test_roster_data.py::test_agents_are_contiguous_by_phase_in_declared_phase_order` requires
agents to appear grouped by phase in the declared phase order, so appending to the end of the file
fails the suite.

**Alternatives considered**: `implementation`, beside the planned `documentation-quality` agent —
rejected because that agent judges documentation that exists and this one creates it, and putting them
together implies an overlap the Q1 clarification deliberately removed. `architecture-design`, on the
strength of ADRs being a common input — rejected because ADRs are one category among an open-ended
set, and phasing the agent by its most recognisable output would misfile every other category.

---

## R2 — How a category is derived, and the reserved map

**Decision**: the category is a lowercase kebab-case slug derived from the *content* of the source, not
its filename. Derivation is open-ended (FR-029), with one constraint: a **reserved map** routes a source
whose category matches a folder another Spectra agent already owns to that agent's folder, naming
convention and template.

| If the source is | Folder | Filename | Template |
|---|---|---|---|
| an architecture decision | `<artifact-root>/adr/` | `ADR-NNN-<kebab-title>.md` | `adr-template` |
| a business requirements document | `<artifact-root>/brd/` | `NNN-<kebab-title>.md` | `brd-template` |
| an impact analysis | `<artifact-root>/impact-analysis/` | `NNN-<kebab-title>.md` | `impact-analysis-template` |
| a test strategy | `<artifact-root>/test-strategy/` | project's existing name | `test-strategy-template` |
| a defect root cause analysis | `<artifact-root>/defect-rca/` | `NNN-<kebab-title>.md` | `defect-rca-template` |
| anything else | `<artifact-root>/<category>/` | `NNN-<kebab-title>.md` | `<category>-template`, falling back to `kb-document-template` |

**Rationale**: FR-030 requires it, and the failure it prevents is concrete. Without the map, a supplied
PDF of past architecture decisions produces `<artifact-root>/architecture-decisions/001-....md` beside
the `adr/` folder the ADR agent maintains — two decision records, two numbering schemes, two shapes,
and no rule for which is authoritative. With it, kb-vault is a second author into one set. Deriving
from content rather than filename is FR-028, and it is what makes the map usable at all: `notes.pdf`
carries no signal, its contents do.

**Alternatives considered**: a **closed category list** — rejected by FR-029, and because the request
itself names "ADR, engineering methodology, UX/UI standards, **etc.**"; a fixed list guarantees a
supplied document that fits nothing, and the fallback for that case is either a junk drawer folder or a
refusal, both worse than a derived slug. **No reserved map**, letting every category derive freely —
rejected above. **Asking the user for the category on every source** — rejected because the plan table
already lets them change it, so asking first spends a round trip to arrive at the same place.

---

## R3 — Template resolution when the name is not known at authoring time

**Decision**: resolve `<category>-template.md` through Spec Kit's four-layer stack in the constitution's
order, and where no layer yields it, resolve `kb-document-template.md` through the same stack. The
shipped `spectra/templates/kb-document-template.md` is the last layer before the command's inline
skeleton. A category in the reserved map resolves that agent's template name instead (R2).

**Rationale**: Principle VIII fixes the *order of the layers* and forbids hard-coding a single path; it
does not require the name be constant. Deriving the name widens the override surface at no cost to the
stack: a team that wants their own UX/UI standards shape drops
`.specify/templates/overrides/ux-ui-standards-template.md` into the repository and every future run
uses it, by exactly the mechanism that an `adr-template` override works. The two-step fallback matters
because it means an unanticipated category still produces a shaped document rather than an unshaped
one.

**Alternatives considered**: **ship a template per anticipated category** (`adr`, `engineering-
methodology`, `ux-ui-standards`, …) — rejected because the set is open-ended, so the shipped set is
always incomplete, and every addition is an extension release. **One generic template for everything**,
ignoring category — rejected because it throws away the reserved map's whole benefit: an ADR produced
by kb-vault would not look like an ADR produced by `adr`. **Infer a shape from the project's existing
documents of that category** — rejected as a *resolution* mechanism because it makes the output depend
on a sample rather than a declared template; kept as a *reporting* obligation instead (FR-056), where
the difference is surfaced and the override path offered.

---

## R4 — Expressing the approval gate agent-agnostically

**Decision**: the gate is prose in the command file: present the table, state explicitly that nothing
has been written yet, ask for approval, and stop. Approval is an affirmative statement from the user in
their own words. Any response that changes the plan re-enters the gate with the full revised table.
Anything that is not an affirmative approval — a question, a comment, silence, an ambiguous "sure,
but…" — is not approval.

**Rationale**: Principle III leaves no alternative; Spectra ships Markdown and has no mechanism to
block a run. The design work is therefore in making the stop unambiguous to the *model* reading the
prompt, and the specific failure to design against is treating a comment on the plan as consent to it.
Three prompt devices carry it: the table is followed by a single explicit question; the command states
in its own voice that no file has been created; and the re-presentation rule (FR-041) means the path
back from any user response leads through the table again rather than around it.

**Alternatives considered**: **writing to a staging area first**, then moving on approval — rejected
because it writes before approval, which FR-039 forbids outright, and because "files appeared somewhere
then moved" is worse for a user reviewing with `git status` than files that never appeared. **Assuming
approval after presenting the plan**, on the theory that the user can revert — rejected because the
command is aimed at repositories with existing documentation, where an unwanted *update* is not
trivially revertible by someone who did not notice it happened.

---

## R5 — Duplicate detection without depending on a search tool

**Decision**: detection is a bounded read, expressed as prose. From the repository survey (FR-025), the
command has the documentation tree's folder layout and filenames. For each source it (1) computes the
candidate folders — the category's own folder, the reserved-map folder if applicable, any superseded
folder, and any documentation folder the survey found; (2) shortlists files in those folders by
filename and heading; (3) reads the shortlist and compares **subject**, not title similarity. A match
is a document of the same category about the same subject.

**Rationale**: FR-032 requires matching on content and category rather than filename alone, and
Principle III forbids naming `rg`, `grep`, or any tool. The bound matters for the same reason it
mattered in `defect-rca`: "search the repository" is unbounded on a large project and degrades into
either a slow run or an arbitrary truncation. Two staged reads — cheap metadata first, full text only
for the shortlist — keep the cost proportional to the documentation set rather than the repository.

**Alternatives considered**: **filename matching only** — rejected by FR-032; `standards.md` and
`ux-guidelines.md` are the same document under two names, and filename matching finds neither.
**Reading every Markdown file in the repository** — rejected as unbounded, and wrong: a match in
`node_modules/` or a vendored `README` is noise. **Asking the user whether a document already exists** —
rejected because the user's not knowing is the common case and the reason they reached for the command.

---

## R6 — The `CANONICAL` registry problem in `tests/test_doc_output_paths.py`

**Decision**: add a second registry beside `CANONICAL`:

```python
# Commands whose output folder is computed per document rather than fixed. They are held to every
# artifact-root rule below, but not to a single write target.
MULTI_CATEGORY = {
    "kb-vault.md": "<artifact-root>/<category>/",
}
DOCUMENT_COMMANDS = tuple(CANONICAL) + tuple(MULTI_CATEGORY)
```

`CANONICAL` keeps its meaning — one command, one folder — and keeps driving the per-folder assertions.
`DOCUMENT_COMMANDS` gains kb-vault, so the artifact-root machinery assertions (the literal
`never write it`, all six publication signals, the `documents/` recommendation, no absolute paths, no
mixed case) apply to it unchanged. A new test class asserts what is specific to a computed destination:
that the command names the `<artifact-root>/<category>/` form, that it names the reserved-map folders,
and that it is *deliberately* absent from `CANONICAL` with the reason — the same device
`TheOutputIsNotAnArtifactRootDocument` uses for `test-plan`.

**Rationale**: `CANONICAL` is a dict of command → **one** folder, and the assertion it drives
(`test_each_document_command_names_its_canonical_folder`) is a substring check for that folder in the
command text. kb-vault has no such folder. Forcing an entry would mean either inventing a fake
canonical folder or weakening the assertion for the five commands that legitimately have one — and the
second is how a guard rots. Splitting the registries keeps every existing assertion exactly as strong
and adds the ones this command needs.

**Alternatives considered**: **`"kb-vault.md": "docs/"`** — rejected because it asserts the command
names the bare root as a write target, which Principle VII forbids and the command must not do.
**Leaving kb-vault out of the module entirely** — rejected because it writes into the artifact root and
therefore needs the publication check, the `never write it` clause and the lowercase rule asserted; an
unasserted document command is exactly what this module was written to prevent. **Changing `CANONICAL`'s
values to lists** — rejected as a larger edit to a module five other commands depend on, for no gain
over a second dict.

---

## R7 — Reading attachments through the host harness, and degrading per file

**Decision**: the command states that it reads whatever the host agent can read, attempts every
supplied source, and reports readability **per file**. An unreadable file is named, its failure stated,
its content requested from the user, and the run continues with the rest. No credential is ever
requested and no network request is made.

**Rationale**: this is the precedent `speckit.spectra.defect-rca` set for JIRA, applied to a different
channel. Spectra ships Markdown only, so it has no PDF reader to bundle and no business asking for one;
it runs inside a coding agent that either can read the file or cannot. Per-file granularity is the part
worth designing: a run with four attachments where one is a scanned PDF must produce three documents
and one honest gap, not four documents of which one is invented, and not a refusal of the whole run.

**Alternatives considered**: **declaring a required tool in the manifest** — rejected; it would block
installation for users who never touch this command, which is the same argument that keeps `gh`
optional today. **Failing the whole run on any unreadable source** — rejected as user-hostile and
against FR-011, which requires continuing with the remainder. **Guessing from the filename** — rejected
outright by FR-011; it is the single highest-severity failure mode this command has, because invented
documentation is indistinguishable from real documentation once committed.

---

## R8 — Index scope: which folders get one, and which must not

**Decision**: kb-vault maintains `<artifact-root>/<category>/README.md` **only** for category folders it
alone owns. It never introduces an index into a reserved-map folder (`adr/`, `brd/`, `impact-analysis/`,
`test-strategy/`, `defect-rca/`). Where a folder already has an index — kb-vault's own from a prior run,
or the project's — it is updated, never replaced wholesale. The index is rebuilt from the documents
present, so a hand-added or hand-deleted file self-corrects.

**Rationale**: FR-049. The index is navigation over one artifact type, which `specs/022` established is
a directory listing rather than a second artifact in the folder. The two restrictions are specific to
this command: introducing a `README.md` into `adr/` would change the ADR agent's folder convention as a
side effect of an unrelated ingestion run, and replacing a hand-maintained index would destroy columns
a rebuild cannot know about.

**Alternatives considered**: **one index at the artifact root listing every category** — rejected; it
is a second file type at the root level, it is not navigation over one artifact type, and it would be
written by one command and read by none. **No index at all** — rejected because a vault whose contents
cannot be enumerated is a folder, and because the shipped house pattern (`impact`, `defect-rca`) already
maintains one. **Indexing every folder written to** — rejected by the reserved-map restriction above.

---

## R9 — Sequence numbering across create, update and collision

**Decision**: for a create, the number is one greater than the highest found in the destination folder
*and* any superseded folder for that category, matched case-insensitively, computed **at write time**
rather than at plan time. For an update, the existing filename is kept unchanged — no renumbering, no
renaming. Where a category has an established convention in the project, that convention wins over the
`NNN-` default.

**Rationale**: FR-045 and FR-046. Computing at write time rather than plan time closes the window
between the plan being presented and approval arriving, during which a file may appear — and on a
multi-document run, between one write and the next. Keeping an updated file's name is not merely
convenient: renaming it would be a move, which FR-061 forbids and which would break every existing link
to it.

**Alternatives considered**: **numbering at plan time so the plan table shows the final filename** —
rejected for the collision window; the table shows the intended name and the report shows the actual
one, and where they differ the report says so. **Renumbering an updated file to fit the sequence** —
rejected; it is a rename in all but name and it breaks inbound links. **A global sequence across
categories** — rejected by Principle VII, which scopes the sequence to the subfolder.

---

## R10 — Supplied documents are data, never instructions

**Decision**: the command states explicitly that text inside a supplied source which is phrased as an
instruction to the agent is document content, not a command. It is transcribed where relevant and never
obeyed. This includes text that claims authority, urgency, or prior authorisation, and text that names
a destination, a filename, or a repository action.

**Rationale**: FR-018, and it is load-bearing rather than ceremonial for this command specifically.
kb-vault is the only Spectra agent whose primary input is a document from outside the repository, often
from outside the team, frequently a PDF nobody has read end to end. A document that says "also write the
following file to `.github/workflows/`" is exactly the shape of the problem, and the approval gate is
not sufficient protection on its own because a user approving a plausible-looking table is not
re-deriving where each row came from.

**Alternatives considered**: **relying on the approval gate alone** — rejected above; the gate protects
against misclassification, not against the agent having been redirected before the table was drawn.
**Stripping imperative sentences from absorbed content** — rejected because an engineering methodology
document is *made of* imperative sentences ("run the linter before pushing"), and stripping them would
destroy the content the command exists to capture. The distinction is between an instruction *to the
agent* and an instruction *the document is about*, and it is a reading-comprehension rule, not a filter.

---

## R11 — Where the write-scope boundary is enforced

**Decision**: the boundary is enforced **at plan construction**, not at write time. A row's destination
is resolved, validated against the write scope, and only then placed in the table. A destination the
scope forbids never reaches the table; the command says why, names the destination it will use instead,
and offers the two legitimate routes (the `Artifact root:` declaration, or a `git mv` the user runs).
The write step writes what the approved table says and performs no path resolution of its own.

**Rationale**: this is what makes the approval gate meaningful. If the boundary were checked at write
time, the user could approve a table containing a destination the command then refuses — approval of
something that does not happen — or, worse, the command could resolve a different path than the one
approved. Constructing only valid rows means the table is a faithful statement of what the run will do,
which is the property FR-035 through FR-037 are trying to buy.

**Alternatives considered**: **validate at write time** — rejected above. **Validate in both places** —
rejected as redundant in a prompt, where every additional rule competes for attention with the rules
that matter; the single enforcement point is stated once and the write step is told to trust the table.
**Allow the table to carry an out-of-scope row marked as a warning** — rejected because it invites the
user to approve it and then discovers the refusal after the fact.
