# Research: An Interactive Domain Analyzer That Feeds the Constitution

No NEEDS CLARIFICATION remained in Technical Context. Each entry below records a design decision the spec
leaves to the plan.

## R1 — Filename

- **Decision**: keep `<artifact-root>/DOMAIN_ANALYSIS.md`.
- **Rationale**: it already sits under `docs/` beside `TEST_STRATEGY.md`, which is the consistency the user
  asked for. Principle VII names it as a singleton, and `review-pr`, `kb-vault`, and `deployment-strategy` read
  it by name. The content is still an analysis — domain, lens findings, decisions.
- **Alternatives**: `DOMAIN_GUARDRAILS.md` (says what it feeds, but needs a MINOR constitution amendment, a
  second earlier location to read, and three reader updates); `DOMAIN_PROFILE.md` (vaguer).

## R2 — Question unit

- **Decision**: one question per lens, plus the domain first — eight in total, fixed.
- **Rationale**: one question per guardrail could exceed 30 turns. A fixed count can be announced honestly, as
  `test-strategy` does. Numbering candidates within a lens (`3.1`, `3.2`) keeps per-item control through free
  text.
- **Alternatives**: one per guardrail (too long); one batch question (forces the domain correction to be
  ignored by later questions).

## R3 — Option set

- **Decision**: Recommended set · Codify only what exists · Full set · Skip. A duplicate is replaced by
  Choose individually. A lens with nothing to propose becomes a four-option confirmation.
- **Rationale**: meets "at least four, one recommended, one Skip" with options that genuinely differ. The
  "codify only what exists" option is the natural brownfield choice and maps directly to R5.
- **Alternatives**: free-form options per lens (inconsistent between runs and hard to test); "stricter /
  lighter" (no objective meaning).

## R4 — Skip, silence, and "use your defaults"

- **Decision**: Skip, an unanswered question, and `--non-interactive` adopt nothing. "Use your defaults"
  takes the recommendations.
- **Rationale**: the answer becomes governance, so silence is not consent. "Use your defaults" is an explicit
  instruction, so it counts as a choice.
- **Alternatives**: `test-strategy`'s rule (unanswered = recommended) — appropriate where the answer only
  shapes a document, not here.

## R5 — `observed` / `aspirational`

- **Decision**: every candidate carries one, settled by reading source code, not documentation.
- **Rationale**: on a brownfield project the SME's key question before ratifying a rule is whether the code
  already meets it. An aspirational rule creates debt on day one; that should be a visible choice.
- **Alternatives**: confidence alone (conflates "how sure is the agent" with "does the code comply").

## R6 — Testing and deployment

- **Decision**: refer, never propose; cite the sibling document if present, name its command if not.
- **Rationale**: `test-strategy` and `deployment-strategy` each draft their own constitution amendment. Two
  sources for one clause is how a constitution contradicts itself.
- **Alternatives**: propose and de-duplicate later (pushes conflict resolution onto the SME).

## R7 — Handoff wording

- **Decision**: two ready-to-paste lines — create (no constitution) or amend (constitution exists) — both
  pointing at the Constitution input section; no line when it is empty. Never invoked.
- **Rationale**: `/speckit-constitution` behaves differently for creation and amendment; the create prompt also
  points it at the Inferred domain section for the project's purpose. Not invoking keeps the SME in their own
  governance change and keeps the command portable (Principle III).
- **Alternatives**: one generic prompt (leaves `/speckit-constitution` to guess); invoking it (not portable).

## R8 — Legacy checkbox files

- **Decision** (clarified 2026-10-23): a `- [x]` item is `accepted`; a `- [ ]` item is **undecided** — recorded `not_asked` — and is
  offered again in its lens's question, marked "unticked in the earlier version". IDs, wording, and `status`
  are kept; the file is rewritten in the new format.
- **Rationale**: the old format cannot distinguish "reviewed and rejected" from "never reviewed". Asking again
  costs one answer per lens; wrongly declining loses the guardrail silently.
- **Alternatives**: unticked = declined (the 1.22.0 command's own rule, but unsafe for never-reviewed files);
  declined only if the file has at least one tick (a heuristic that still misreads partial reviews).
- **Status**: not yet reflected in the working tree — see the plan's Evidence table.
