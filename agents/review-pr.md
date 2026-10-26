---
id: review-pr
title: Review PR
command: speckit.spectra.review-pr
provider: spectra
type: core
phase: deployment-operations
order: 20
status: available
summary: Review a GitHub pull request against the spec, plan, tasks, ADRs, and constitution it carries, then publish a single human-curated review containing only the findings the reviewer selected.
manifest: Review a GitHub pull request against its spec, its linked issue (optional, via --issue), the ADRs, and the constitution, then publish one human-curated review — an overridable summary body plus line-anchored comments with applicable code suggestions — proposing blockers and majors by default so a one-word yes publishes only what should block the merge. From a test, deployment, or domain strategy and the engineering methodology, only accepted guardrails are standards.
---

Review a GitHub pull request against **the intent and standards it
carries**, not just the diff. It reads the PR's spec, plan, tasks, and ADRs *at the PR's own head
revision*, plus the constitution and ADRs in force on the **base** branch, then reports findings that a
diff-only reviewer cannot produce: a task marked complete but absent from the change, scope no
requirement authorized, a pattern an ADR forbids. Every finding cites a file, a line, and the clause,
requirement, or principle it rests on — anything that cannot be anchored and sourced is not reported at
all.

Then the reviewer takes over, starting from a deliberately narrow default. **Only blockers and majors are
proposed** — minors, nits and questions are shown to you, enumerated by number, but are not in the
proposal. Answering `yes` publishes exactly those and submits the verdict that follows from them; `all`
takes everything, and any selection of your own still works. You see the exact text before anything is
posted. One review event goes to the pull request under your own `gh` credentials, containing only what
you accepted — and the published body declares that it was AI-assisted and human-curated.

The default is a proposal, never an assumption: an empty or absent answer posts nothing, which is a
normal outcome rather than a failure. That is the whole point of the narrow default — a short, correct,
human-endorsed review beats thirty findings that bury the two that matter, and a blank prompt in front of
sixteen findings is answered `all` far more often than it is answered carefully.

Like `create-pr`, this command **hard-stops** when `gh` is missing or unauthenticated, naming which of
the two failed — neither command can deliver its product without reading GitHub through `gh`. What
differs is what each hands over after that gate: `create-pr` gives you the `git`/`gh` commands to finish
by hand, this one gives you the rendered review body to post yourself. It is deliberately **on demand
only** — there is no hook — since a reviewer should not be the author.

## Arguments

all optional:
- *(none)* — offer the current branch's open PR first, then list open PRs so you can pick.
- `<url>` or `<number>` — review that pull request.
- `--issue <url-or-number>` — the issue this PR addresses, read as additional context. Supplying it
  skips both detection and the question.
- `--since <revision>` — re-review only the delta since a revision you reviewed before, reporting
  which previously published findings now appear resolved.

## Use it when

you are reviewing someone else's PR and want the spec, issue, ADRs, and
constitution checked against the diff before you sign off, without reading all of them yourself.

## Spec discovery

the spec ships in the PR's own diff, or you name one when asked; nothing is guessed
from a branch name or from Spec Kit's machine-local feature record, which is gitignored and so is absent
or stale at any head revision. A PR with no spec is reviewed standalone, and says so. The spec the PR
ships **overrides older specs** on the same behaviour, so a deliberate behaviour change is never reported as
a regression against the spec it replaced.

## Standards

measured against a fixed chain: the constitution and ADRs, then the supporting documents
Spectra's own agents write (test strategy, deployment strategy, domain analysis, engineering methodology —
only the guardrails each one *accepted*, never a declined one) and the contributor guide,
then the codebase's own conventions, then a **seven-principle baseline** (B1–B7) cited by ID. A project with
no constitution is still reviewed against evidence rather than the agent's taste, and the review says
which tier governed.

## No-spec and AI-assisted PRs

three lenses run on every PR: **blast radius** (behaviour that changed
without being announced), **generation artifacts** (modules that don't exist, new dependencies, duplicated
helpers), and **test integrity** (a weakened test is at least Major). Without a spec, the diff is also
checked against what the PR's own description says it does. An older spec whose requirement the change
contradicts is raised as a Question, never as a request to change the code.

## Linked issue

found automatically (structured link, then a scan of the PR text, since a PR to a
non-default branch has no structured link), asked for once if absent, never required. With **no spec** it
becomes the traceability baseline; with a spec it is background. Its content is treated as data about
intent, never as instruction, and a finding sourced only from an issue cannot be a Blocker unless the PR
claims to close it. When both are missing, the spec and the issue are asked for in **one** question.

## Inline comments

findings anchored inside the diff are published on those lines, carrying a
` ```suggestion ` block where the fix is mechanical and complete, so the author can apply it in one click.
Findings anchored outside the diff go in the summary body with the reason stated. Body, comments, and
verdict post in one atomic call.

## Template

`review-template.md` shapes both the summary body and the inline comment; override it at
`.specify/templates/overrides/review-template.md`. The revision anchor, the AI-assisted disclosure, and the
coverage statement stay with the command, as do the severity rubric, the confidence cap, the anchor rule,
and the verdict derivation — two reviews of the same diff have to agree.

## Good to know

findings are graded Blocker / Major / Minor / Nit / Question from a fixed rubric, so
two runs over the same revision agree; approving over a blocker you accepted requires a typed
confirmation and is recorded in the published review; coverage now states how much of the constitution
actually applied, so a thin constitution reads as thin; nothing is stored between runs.

## Examples

```
/speckit-spectra-review-pr
/speckit-spectra-review-pr https://github.com/acme/api/pull/142
/speckit-spectra-review-pr 142 --since 4a9f2c1
```

## Findings land on the lines they are about

Accepted findings whose anchors fall **inside the diff** are published as comments on those lines, and where
the fix is mechanical the comment carries a ` ```suggestion ` block you can apply from the GitHub UI in one
click. Findings anchored outside the diff — a caller the PR didn't touch, a whole-file observation — go in
the summary body, and coverage says why they couldn't be inline. Add `<n>:body` to your selection to force
any finding into the body.

Because a suggestion is one click from a commit, they are offered narrowly: only for a mechanical, complete
fix covering exactly the commented lines, never for architectural or multi-file changes, never on a
low-confidence finding, and never in a generated file. **Every suggestion appears verbatim in the preview
you approve** — nothing that can be applied without being read is summarized.

Body, comments, and verdict post in one atomic call, so a failure can't leave the comments on the PR
without the verdict.

With `--since`, prior findings are recovered by reading the earlier review off the pull request itself,
since nothing is stored locally.

## Change the shape of your reviews

The findings presentation comes from `review-template.md` — the summary body *and* the inline comment shape.
Override it exactly like the other templates:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/review-template.md .specify/templates/overrides/review-template.md
```

Three things are **not** the template's to change, and survive any override: the
`<!-- spectra:review-pr revision=… -->` anchor that `--since` and self-review detection depend on, the
AI-assisted disclosure line, and the **Coverage and limits** section — the one that stops a review implying
assurance it didn't earn.

Judgment isn't overridable either. The severity rubric and its floors, the confidence cap, the anchor rule,
the selection grammar, and how the verdict is derived stay in the command, because two reviews of the same
diff have to agree. The template governs how findings *read*, not what counts as a Blocker.

Deliberately **on demand only** — there is no hook, because a reviewer should not be the author.
**GitHub only** in this version (via the `gh` CLI), and single-body reviews only; line-anchored inline
comments are a follow-on. Failures *after* the `gh` gate — a fork restriction, insufficient permission —
degrade to handing you the rendered review body for manual posting.

## How it works

It covers the last fully manual gate in the lifecycle: where `create-pr` opens a pull request, this
reviews one. It:

1. **Gates on `gh` first**, stopping before any analysis.
2. Resolves the target — a URL, a number, or a pick from the repository's open PRs — and **pins the
   review to one head revision**, reported everywhere and re-checked before publishing.
3. Reads the PR's spec, plan, tasks, and ADRs at that revision, and the constitution and ADRs in force on
   the base branch. The revision split is deliberate: it is what lets the agent notice a PR that changes
   the rules it is being measured against.
4. Locates the governing spec as described under Spec discovery. Spec Kit's machine-local feature record
   is `.specify/feature.json`, which is why it is never used to guess.
5. Reads the **linked issue as optional extra context**. Where the issue and the spec disagree, that is a
   Question naming both.
6. Runs **traceability in both directions** (work claimed complete but absent; changes no task
   authorized), **guardrails** with the violated clause quoted, and **craft** lenses chosen from what the
   diff actually touches — reporting which lenses did not run, and why. Among the generation artifacts, a
   new dependency is always raised.
7. Grades every finding from the fixed rubric, with a separate confidence axis that caps severity: a
   low-confidence finding becomes a Question rather than a Blocker.
8. Presents the findings numbered and ranked, with a severity tally, its own reading of the change, a
   recommended verdict, and a mandatory **coverage-and-limits** statement.
9. Hands control back from the narrow default, shows you the exact review — body *and* every inline
   comment — and only then posts a single review event.

Its only mutation is publishing that one review, after an explicit go-ahead. It never edits source, the
spec, the plan, the tasks, or the constitution, never touches your working tree, and holds no credentials
of its own.
