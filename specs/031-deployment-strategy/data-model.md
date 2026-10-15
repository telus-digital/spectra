# Data Model: Deployment Strategist Agent

The agent persists exactly one thing: the document at `<artifact-root>/DEPLOYMENT_STRATEGY.md`. These
are the entities that document carries, and the rules each must satisfy. Field names in `code` are the
front-matter keys; the rest live in the body.

## Deployment strategy document

| Field | Type | Rule |
|---|---|---|
| `mode` | enum `greenfield` \| `brownfield` \| `mixed` | from deployment practice (research R2), never asked |
| `generated` | ISO-8601 timestamp with offset | time of the write |
| `template` | string, project-relative path or `inline` | the resolved template layer (FR-037) |
| `run` | integer ≥ 1 | prior document's `run` + 1, else 1 |
| `deployables` | list of Deployable (short form) | at least one; see below |
| `coverage_of_analysis` | quoted string | what was read out of what is present (FR-025) |
| `amendment_state` | enum `embedded` \| `partial` \| `absent` \| `none` \| `not_asked` | one word; detail in the body |
| `clarification` | Clarification record | always all five entries |

Validation: front matter parses as YAML — every free-text value quoted, no key holding both a scalar and
a collection, enumerations spelled exactly (FR-039). Body sections follow the resolved template.

## Deployable

| Field | Type | Rule |
|---|---|---|
| `name` | quoted string | workspace or directory name |
| `root` | quoted project-relative path | `"."` for a single-deployable project |
| `class` | enum `service` \| `static-site` \| `library` \| `cli-desktop` \| `mobile` \| `infra` | research R1 |
| evidence (body) | list of citations | the deciding signals, plus dissenting ones |

A project with one deployable says so once; it does not repeat per-deployable headings.

## Lens finding

One per deployable per mandatory lens (six), plus one per conditional lens the evidence warrants.

| Field | Rule |
|---|---|
| lens | one of the six mandatory lenses, or a named conditional lens with its warranting evidence |
| applicability | `applicable` or `not applicable` + one-line reason; never omitted (FR-012) |
| current state | brownfield/mixed: reported first, each claim with a provenance (FR-013) |
| recommendation | each with exactly one provenance (FR-021) and, where possible, the exact change the team would make |
| re-run mark | `new` \| `adopted` \| `carried` on a re-run (FR-042) |

Lens-specific obligations: environments & promotion carries one Mermaid diagram bound to its table
(research R7); pipeline cites `TEST_STRATEGY.md` for which tests exist or records its absence as a gap
(FR-015); data & schema change states app rollback ≠ DB rollback (FR-017); rollback & recovery marks each
recovery claim drilled or assumed (FR-018); operability lists and links existing jobs and alerts without
redefining them (FR-019).

## Provenance

Enum `verified` \| `claimed` \| `stated` \| `convention` (research R5).

| Value | Carries |
|---|---|
| `verified` | project-relative path, optional line, to what the repository does |
| `claimed` | path to the asserting document (in or outside the repository) |
| `stated` | the clarification question number |
| `convention` | nothing; the absence of project evidence is the point |

An absence claim additionally names what was searched and where (FR-022).

## Clarification record

Exactly five entries, keyed `n: 1..5`, in the front matter and repeated in the body (FR-039, FR-040).

| Field | Type | Rule |
|---|---|---|
| `n` | 1–5 | fixed order (research R4) |
| `ask` | quoted string | the question as asked, or as a confirmation |
| `recommended` | quoted string | the marked option |
| `answer` | quoted string | the answer taken; may carry a per-deployable split |
| `disposition` | enum `answered` \| `default_taken` \| `not_asked` | non-interactive and unanswered → `not_asked`; "use your defaults" → `default_taken` |

Counts `asked` and `answered` sit beside the list.

State transitions within a run: *pending* → *asked* → (*answered* \| *default_taken*); *pending* →
*not_asked* (non-interactive, or unanswered). A reply that is not an answer leaves the entry *asked*.

## Open question

| Field | Rule |
|---|---|
| item | what is unknown (identifier, owner, target) |
| who answers | client, ops owner, platform team, security — a role, never a guessed person |
| blocks | which lens or recommendation waits on it |

Never carries an invented value (FR-024).

## Proposed amendment

| Field | Rule |
|---|---|
| state | `embedded` \| `partial` \| `absent` \| `no constitution` with the governing clause quoted where one exists |
| conflict | any existing principle a recommendation contradicts, as its own finding (FR-046) |
| items | unchecked `- [ ]` statements in the constitution's voice, each with `section:` and `status: add` or `amends: <principle>` |
| scope | durable invariants only (research R8); the reference-the-document item included |
| approval | `approved` \| `declined` \| `not_asked`; only `approved` records items |
