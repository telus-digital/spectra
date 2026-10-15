# Contract: Clarification Round

Runs after reading, classification, and root resolution; before the template is resolved and the
lenses are worked (FR-026).

## Announcement (once, before question 1)

> Five judgment calls the repository cannot settle, one at a time. Answer several at once if you already
> know them, say **use your defaults** to take every recommendation and skip the rest, or skip any single
> question.

## The five questions (fixed order, once per project)

| # | Asks | Recommendation source / confirmation trigger |
|---|---|---|
| 1 | Where this project is hosted or published | research R4 row 1 |
| 2 | Who approves a production deploy, and how | research R4 row 2 |
| 3 | Whether a stakeholder-review / pre-release environment exists or is wanted | research R4 row 3 |
| 4 | Availability and RPO/RTO targets | research R4 row 4 — never an invented number |
| 5 | Release cadence | research R4 row 5 |

## Shape of each question

```text
Question N of 5 — <question>

<one line naming any difference between deployables, if there is one>

  A. <option>
  B. <option> (recommended)
  C. <option>

Recommended because: <project-relative path or document>, or "convention, nothing in this project".
These options are scaffolding — answer in your own words if none fits, per deployable if they differ.
```

- 2–4 labelled options, exactly one marked recommended (FR-028).
- One question per turn; end the turn and wait.
- Where evidence settles it: same number, phrased as a confirmation (FR-029).

## Replies

| Reply | Effect |
|---|---|
| an option, or free text | `answered`; next question |
| several answers at once | each `answered`; skip to the first unanswered |
| "use your defaults" (or equivalent) | current and remaining → `default_taken`; round ends |
| skip / no answer | recommendation taken; `not_asked` |
| a question or comment | answer it; re-ask the same question; no advance |

## Re-run

Each question opens with the prior recorded answer as the proposed answer ("last run you said X; still
true?"). A prior `not_asked` is asked normally (FR-033).

## Non-interactive

Declared only (`--non-interactive`, or the user saying no answer can be given). Announce once; ask
nothing; every entry `not_asked` with the recommendation as the answer (FR-032).

## Record

All five entries in front matter and body: `n`, `ask`, `recommended`, `answer`, `disposition`; plus
`asked` and `answered` counts (FR-039, FR-040).
