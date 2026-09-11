# Phase 0 — Research: Defect Root Cause Analysis Agent

**Feature**: `022-defect-rca-agent` | **Date**: 2026-09-11 | **Plan**: [plan.md](./plan.md)

The Technical Context carries no `NEEDS CLARIFICATION`: the stack is fixed by Principles II, III and
VIII — a Markdown command file, a registered template, no scripts, no binaries. Research here is about
the gap between a specification that says *what* must be true and a command file that has to say *how*.
Eight decisions follow. Five are new; three are deliberate reuses of mechanics
`spectra/commands/impact.md` already solved, recorded so the reuse is a decision rather than a
coincidence.

---

## D1 — Channel detection is shape-based, stated, and correctable

**Decision.** The command classifies `$ARGUMENTS` by form, in this order, and **states the channel it
resolved to before gathering any evidence** (FR-008):

| Form observed | Channel |
|---|---|
| A URL on a GitHub host containing `/issues/<n>` | GitHub issue |
| A bare `ABC-123` token, or a URL containing `/browse/ABC-123` or `atlassian.net` | JIRA |
| Anything else, including prose that happens to mention a ticket | Plain description |
| Empty | None — ask, and stop (FR-009) |

Ambiguity resolves toward *plain description*, which is the channel that cannot fail. A user who meant
the ticket can say so in one word, because the resolved channel was announced.

**Rationale.** Announcing the classification is the cheap half of the decision and does most of the
work: misclassification is self-correcting the moment it is visible, and silently invisible otherwise.
Defaulting ambiguity to prose rather than to a retrieval attempt also keeps the failure modes out of the
common path — the plain channel makes no outbound request, prompts nothing, and always proceeds.

**Alternatives rejected.** *Ask which channel this is* — a question the argument's shape already
answers, and FR-028's spirit forbids asking what can be determined. *Try retrieval on anything
URL-shaped* — turns a typo into a network attempt and a confusing error. *Require a flag
(`--jira`, `--issue`)* — a flag every user would have to learn to avoid a misread that announcing the
classification already catches.

---

## D2 — A recurrence match is a claim about evidence, made on three axes, never on the title

**Decision.** FR-020's search runs on three axes, each of which can produce a match on its own:

1. **Symptom overlap** — the observable failure, normalized (an HTTP status, an exception type, a
   timeout, a data-corruption shape), compared against the prior document's symptom line and problem
   statement.
2. **Implicated code overlap** — a file or module named in the prior document's evidence table also
   appears in this defect's traced code paths. This is the strongest axis, because it is the only one
   grounded in something neither document's author phrased.
3. **Root-cause overlap** — the prior document's validated root cause names a mechanism this defect's
   hypothesis tree also contains.

Every surfaced match is presented with **which axis fired and what the overlap was**, so the user can
dismiss a spurious one in a sentence. Title similarity is explicitly not an axis; it may order results
but never produce a match.

**Rationale.** The BRD's risk register names both failure directions — a growing corpus that misses
matches, and one that surfaces spurious ones — and a single similarity score fails in both at once
without telling anyone why. Three named axes make a match auditable: "same file" is a fact the user can
check, "similar title" is not. Excluding title is what the BRD asks for in Section 15's rationale, and
it is why the slug describes the *symptom* rather than the cause (D5).

**Alternatives rejected.** *A similarity score with a threshold* — unauditable, untunable by a prompt,
and the threshold would be a magic number nobody could justify. *Exact-match on a normalized symptom
string* — misses everything real; the same defect is rarely described twice the same way. *Ask the model
to "look for anything similar"* — produces confident matches with no stated basis, which is the spurious
half of the BRD's risk.

---

## D3 — Preventive-action completion is a three-valued assessment, and "undeterminable" is the default

**Decision.** For each preventive action on a surfaced prior RCA, FR-022 requires one of exactly three
verdicts:

- **Apparently completed** — permitted *only* with a citation: the test that now exists, the commit that
  made the change, the configuration that now holds, the code that now validates.
- **Apparently not completed** — permitted only with a citation of the absence: what was searched for,
  where, and what was found instead.
- **Undeterminable** — the default, with the reason stated: the action is organizational, or it names an
  artifact outside this repository, or the evidence is runtime-only.

The command never emits a bare "done" or "not done".

**Rationale.** This is the most load-bearing judgement the command makes, because it is the one that
tells a user whether they are looking at a new defect or a fix that never landed — and it is the one
most likely to be wrong. An uncited "completed" on a preventive action that was never finished actively
suppresses the recurrence signal the whole feature exists to raise. Making "undeterminable" the default
and citations mandatory for the other two inverts the risk: the command under-claims and the human
checks, rather than the command over-claims and nobody does.

**Alternatives rejected.** *Two-valued done/not-done* — forces a guess on organizational actions
("establish a review practice") that no repository can answer, and the guess will read as a finding.
*Skip the assessment and just surface the prior actions* — BR-29 asks for it, and the case it exists for
is precisely a recurrence following an incomplete fix. *Ask the user each time* — spends the question
budget on something the repository can often answer, against FR-028.

---

## D4 — The ladder is kept honest by naming the layer and by forcing a systemic pass

**Decision.** FR-026's five layers — symptom, immediate technical cause, contributing factors,
process/practice gap, systemic/organizational root cause — are enforced by three prompt mechanics:

1. **Every probe states its layer.** Not as decoration: a session whose probes are all at layers one and
   two is visibly shallow to the user while it is still cheap to fix.
2. **A plausible code path is a layer-two finding, never a conclusion.** The command explicitly names
   what it found *and* asks what allowed it to reach production — the missing test, the review that did
   not catch it, the configuration that was never validated.
3. **Synthesis is blocked at layer two.** Where the deepest validated finding is an immediate technical
   cause, the command says so and names what would be needed to go further, rather than writing a
   document whose "root cause" is a restated symptom.

**Rationale.** The BRD's risk register calls this out directly: code analysis produces *false
confidence* — the agent finds a plausible path and stops. That is the specific failure mode an agent
with repository access has and a human questioner does not, because the plausible path is genuinely
there and genuinely related. SC-002's 80% bar is only reachable if stopping is made visibly incomplete
rather than quietly acceptable.

**Alternatives rejected.** *Require exactly five whys* — mechanical, and produces padded layers when the
chain is genuinely three deep. *Let the model decide when it is deep enough* — this is the failure mode,
not the fix. *Refuse to write below layer four* — punishes the honest case where the evidence truly ran
out; FR-039f's "nothing validated, here is what would settle it" is the better shape.

---

## D5 — The slug names the symptom, and the number carries identity

**Decision.** `NNN-<slug>.md` where the slug is three to five words describing the **observed problem**,
never the suspected cause (FR-043) — `order-submission-500s`, not `missing-connection-pool-limit`. The
number is one greater than the highest present in the folder, not a count of files.

**Rationale.** The file is named before the analysis concludes. A cause-named file is wrong whenever the
analysis lands somewhere unexpected, which is the interesting case; a symptom-named file stays accurate
regardless and is what makes the flat directory scannable — which is what makes the recurrence search of
D2 cheap. Highest-plus-one rather than count means a deleted or archived document cannot cause a
collision.

**Alternatives rejected.** *Ticket key as the filename* (`PROJ-1234.md`) — breaks the plain-description
channel entirely and makes the corpus unreadable without JIRA access. *Date-prefixed* — sorts the same
as the sequence but carries no identity to reference from another document's related-RCA field. *Cause
in the slug* — wrong exactly when it matters.

---

## D6 — Root resolution, write-once, numbering, secrets and non-interactive mode are taken from `impact` verbatim

**Decision.** Five mechanics are reused from `spectra/commands/impact.md` rather than re-derived, with
only the artifact name changed:

| Mechanic | Reused as |
|---|---|
| Declared-root-wins, publication-signal check, offer-the-line-never-write-it | FR-040 – FR-042 |
| Four-layer template resolution with the inline skeleton last, resolved path reported | FR-050, FR-052 |
| Write once at the end; number resolved at that moment; an abandoned run consumes nothing | FR-043b |
| Secrets located and described by kind and location, never quoted | FR-039e |
| Non-interactive mode: proceed, record what was unanswered, state the confidence cost | FR-031 |

**Rationale.** These are solved problems whose failure modes are already understood, already pinned by
`tests/test_doc_output_paths.py` and `tests/test_document_templates.py`, and already familiar to anyone
who has read another Spectra document agent. A second phrasing of the same rule is a second thing to
keep in sync and a second place for a subtle divergence to hide. Reusing the wording means the existing
assertions apply to this command the moment it joins `CANONICAL`.

**Alternatives rejected.** *Shared prose in a common file the commands include* — Spec Kit installs
command files individually; there is no include mechanism, and inventing one breaks the Markdown-only
guarantee. *Paraphrase for this domain* — the divergence risk with no benefit.

---

## D7 — One command, five modes, and session state that lives in the conversation

**Decision.** All five BRD journeys ship as one command file with modes reached by what the user says,
not by separate commands or flags: intake → loop → synthesis is the spine; issue-tree exploration is
reachable with no defect in hand; reflection is offered after synthesis. State between turns — the
hypothesis tree, statuses, closed and open gaps, the analysis layer — is **carried in the conversation
and re-rendered**, never written to disk (FR-036).

**Rationale.** Splitting into `defect-rca-intake`, `defect-rca-synthesize` and so on multiplies the
command surface for one capability and forces state onto disk to cross the boundary — which would mean
a second artifact type, a second folder, and Principle VII engaged twice for something that is not a
deliverable. One command keeps the loop where it belongs: in a conversation, which is the medium the
loop was always going to run in. Re-rendering rather than persisting also means the user can edit the
tree by saying so, which is what BR-14's "edit, annotate" actually asks for.

**Alternatives rejected.** *A command per journey* — five roster entries for one capability, and a
state-passing problem that only a file can solve. *A session file under `.specify/`* — writes outside
the declared scope, survives past its usefulness, and turns an abandoned analysis into litter.
*Flags to select a mode* — the modes are reached by saying what you want; a flag is a manual to read.

---

## D8 — The question budget is five per round, prioritized by what would change the analysis

**Decision.** At most five questions per round (matching `impact`'s cap), ordered by which answer would
most change the current hypothesis ranking, with the *reason it matters* stated alongside each. The
root-resolution question of FR-041 does not count against the budget — it is about where to write, not
about the defect. Reaching the cap is a disclosure, never a silent truncation.

**Rationale.** FR-029 requires prioritization rather than exhaustiveness, and a cap is the only thing
that makes prioritization real — an unbounded list is never ordered, because nothing is left out. Five
matches the house number and is about what a person will actually answer in one sitting. Saying *why*
each question matters is what lets a user answer three and skip two deliberately rather than
abandoning the round.

**Alternatives rejected.** *Unbounded* — produces the questionnaire the BRD's problem statement names.
*One at a time* — correct for a chat and wrong for a defect, where the human often has to go and fetch
logs; batching lets them make one trip. *A cap on total questions per session* — the loop is iterative
by design, and a session-wide cap would cut off an analysis that is legitimately converging.

---

## Consolidated: what these decisions commit the command file to

- A stated channel before any evidence gathering (D1), and a plain-description path that never fails.
- Three named match axes with the firing axis disclosed (D2), title excluded.
- Three-valued preventive-action verdicts with citations mandatory for two of them (D3).
- A layer named on every probe, and synthesis blocked at layer two (D4).
- Symptom slugs, highest-plus-one numbering (D5).
- Five mechanics lifted from `impact` with wording preserved (D6).
- One command, five modes, zero session files (D7).
- Five questions per round with stated stakes, cap disclosed (D8).
