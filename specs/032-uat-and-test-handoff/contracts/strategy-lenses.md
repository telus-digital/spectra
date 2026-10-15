# Contract: test-strategy — UAT and Regression lenses

Covers FR-001 to FR-007. Each pinned phrase is a sentence the command file MUST contain, matched
case-insensitively after whitespace collapse. Tests assert on these phrases.

## Lens table

The four-lens table becomes six rows. The two new rows:

| Lens | Proves | May assume |
|---|---|---|
| **UAT** | that the feature is acceptable to its user, in the user's own terms | nothing about the implementation — only that the build is assembled |
| **Regression** | that behaviour which already worked still works after a change | the existing suite is the baseline, at whatever level those tests live |

- Pinned: "**six mandatory lenses**". All occurrences of "four mandatory lenses" are replaced.
- Pinned: "Never omit a lens" (unchanged).

## UAT section

- MUST state applicability and its reason.
- MUST state the executor policy: `human`, `agent on explicit request`, or both.
- MUST state the evidence per surface the project has. Evidence for a surface the project lacks MUST NOT
  be named. Pinned: "**evidence for a surface this project does not have is not named**".

## Regression section

- MUST name the gate suite and cite where it runs, or say "runs nowhere automatically".
- MUST state the fixed-defect rule. The default is yes, marked `convention`, unless Q5 says otherwise.

## Clarification round

- Still exactly five questions. Pinned: "Always five" (unchanged).
- Q3 wording gains "or a UAT scenario, and who signs UAT off".
- Q5 wording gains "whether an AI agent may execute UAT here, and against which environments".

## Front matter (additions)

`lenses:` and `ownership:` as in [data-model.md](../data-model.md). They are quoted per the existing
YAML rules, with enumerated values `applicable` or `not_applicable`.

## Amendment clause

Drafted only where UAT is applicable. It goes in the constitution's voice, in the existing
checkbox-and-section format:

```markdown
- [ ] UAT tasks MUST NOT be executed or marked complete by the implement command; they run only on an
      explicit request, by a human or by `speckit.spectra.uat`, so acceptance is never self-certified by
      the agent that wrote the code.
      section: <testing section>
      status: add
```

The invariant "never write the constitution" is unchanged.

## Template

`test-strategy-template.md` gains `## UAT` and `## Regression testing` after `## End-to-end testing`, and
the inline skeleton gains the same two sections. `test_document_templates.py` already checks that the
template and the skeleton agree.
