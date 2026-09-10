# Contract — The Constitution Amendment Handoff

The one place this command touches governance, and the line it does not cross.

## The invariant

**This command never writes `.specify/memory/constitution.md`.** Not on approval, not on a re-run, not
when the file is missing, not when the user insists. There is no code path, no flag, and no state in
which it has permission (FR-032).

What approval authorises is a paragraph in a document the command was already writing, plus a sentence
telling the user what to run next.

## The three states

Determined semantically, never by a string match on "test" (R6, FR-029):

| State | Test | Output |
|---|---|---|
| `embedded` | a principle or standards section states normative testing obligations covering the strategy's core claims | quote the governing clause; **draft nothing** |
| `partial` | testing obligations exist but omit or contradict part of the strategy | quote what exists; draft an amendment scoped to the gap; surface any contradiction as a finding (FR-033) |
| `absent` | no normative testing obligation anywhere | draft a new principle |

**No constitution at all**: report that there is nothing to amend, name `/speckit-constitution` as the
way to create one, and create nothing (FR-030).

## The draft

Reuses `domain-analyzer`'s handoff shape so `/speckit-constitution` consumes one format, not two (R7):

```markdown
- [ ] <statement, in the constitution's voice, MUST/SHOULD, with a brief rationale>
      section: <target section name>
      status: add | amends: <principle name>
```

| Requirement | Source |
|---|---|
| Written in the constitution's voice — declarative, testable, MUST/SHOULD | FR-032b |
| Names the section it targets | FR-032b |
| States whether it adds a new principle or amends an existing one | FR-032b |
| Shown in full **before** the user chooses | FR-031 |
| Unchecked by default; the user's approval is what checks it | `domain-analyzer` precedent |

## The gate

Three paths, offered together, with the text already on screen (FR-031):

| Path | What happens |
|---|---|
| **Approve** | the draft is recorded in the document's proposed-amendment section; the handoff sentence names the `/speckit-constitution` invocation; the constitution is untouched |
| **Modify** | the strategy is revised in place, re-summarised, and the same gate is offered again (FR-035) |
| **Discuss** | the conversation continues; nothing is recorded until one of the other two paths is taken |

**Declined or unanswered**: nothing is recorded and the constitution is byte-identical (FR-032).

**Non-interactive**: the condition is announced once, the document is written, the draft is recorded as
`not-asked`, and no approval is inferred (FR-034).

## The handoff

A sentence, not an invocation. The command tells the user to run `/speckit-constitution` referencing
the strategy document; it does not call it (R7, Principle III).

Two reasons this is a sentence rather than a chained call: an agent-agnostic prompt cannot portably
invoke another command, and chaining would remove the user from their own governance change at exactly
the moment they should be looking at it.

## What `/speckit-constitution` owns and this command does not

- the sync impact report;
- the MAJOR / MINOR / PATCH bump-type judgement;
- the version and Last Amended lines;
- propagating the change into dependent templates and docs in the same change.

Duplicating any of these here would put a second implementation of the amendment procedure in a
command that is not about governance, and its failure mode is a subtly malformed constitution rather
than an obviously broken one.
