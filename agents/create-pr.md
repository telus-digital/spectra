---
id: create-pr
title: Create PR
command: speckit.spectra.create-pr
provider: spectra
type: core
phase: deployment-operations
order: 10
status: available
summary: Open a correctly-targeted GitHub PR for the current spec branch and return its URL.
manifest: Open a correctly-targeted GitHub PR for the current branch — optionally linked to an issue via --issue — with the body built from the overridable pr-template, one final confirmation before anything is created, and the PR URL returned.
---

Open a correctly-targeted GitHub PR for the branch you are on, optionally
linked to an issue, with the body built from an overridable PR template. It asks once with everything on the
table before creating anything, and returns the PR URL. Also offered automatically by an `after_implement`
hook once `implement` finishes, so you don't have to invoke it by hand.

`gh` is required at run time, and the command **gates on it before doing anything else**: if `gh` is
missing or unauthenticated it stops immediately — before reading the constitution, before deriving a base
branch, before touching the remote — and names which of the two failed, because the remedies differ
(install the CLI, or `gh auth login`). Nothing is mutated on that path, and a missing `gh` never produces
a `gh` command you cannot run. A remote that isn't on GitHub stops the same way, with a scope statement.
Failures *after* the gate degrade instead: you get the manual `git push` + `gh pr create` commands with
the derived base branch filled in, plus an explicit statement of whether the branch already reached the
remote.

**Works from any branch** — a `fix/…` or chore branch is fine; only a detached HEAD and a branch that is
already the base are refused. A spec branch simply contributes more to the body (`spec.md`, `plan.md`,
`tasks.md`), while the **Changes** section always comes from the real diff against the base.

**Uncommitted work is offered a commit, not a warning.** A dirty tree gets the file list and the question
*"should I proceed with committing and pushing first?"* — yes behaves like an ordinary commit-and-push, no
opens the PR from committed work and says what was excluded. Credential-shaped filenames are called out
before anything is staged, and `--no-verify` is never used.

## Arguments

all optional:
- *(none)* — open a **ready-for-review** PR (the default).
- `--issue <url-or-number>` — the issue this PR addresses. Omit it and you are asked once; skipping the
  question writes no issue section at all.
- `--draft` — open the PR as a **draft** instead.
- `--base <branch>` — use this base branch (still shown in the final summary).

## Use it when

a piece of work is ready for review and you want the PR opened against the right base,
shaped like your team's template, without running `git`/`gh` by hand.

## Template

`pr-template.md`: Summary, Related Issues, Type of Change, Changes, How to Test, Evidence,
Breaking Changes, Notes for Reviewers — and deliberately **no self-certification checklist**. Override it
at `.specify/templates/overrides/pr-template.md`; the override is committed, team-wide, and survives
extension updates. Trimming **Related Issues** does not unlink the PR: an issue you passed is appended with
a note rather than dropped.

## Linked issues

GitHub honours closing keywords **only** on PRs targeting the default branch, so the
command writes `Closes #42` there and a plain `#42` reference anywhere else, telling you that merging will
not auto-close it. Cross-repository issues are referenced by full URL.

## Base branch

a promotion flow documented in the constitution or the `git` extension config is used
and cited. With nothing documented the command *proposes* a base and asks at the final gate, so you can
answer "no, use dev" without restarting.

## Examples

```
/speckit-spectra-create-pr
/speckit-spectra-create-pr --draft
/speckit-spectra-create-pr --base develop
```

## One thing to know about linked issues

GitHub interprets closing keywords **only when a PR targets the repository's default branch**. On any other
base they are ignored: no link is created and merging closes nothing. So the command writes `Closes #42`
only when the base *is* the default branch. Targeting a `dev` in a promotion flow, it writes a plain `#42`
reference instead — which still records a cross-reference on the issue — and tells you auto-close will not
happen on this merge. An issue in another repository is referenced by full URL, never with a keyword.

## Change the shape of your PRs

The body's structure comes from `pr-template.md`. Override it exactly like the ADR and BRD templates:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/pr-template.md .specify/templates/overrides/pr-template.md
```

Commit it, and every PR the command opens follows your structure — resolution order, the reported template
path, and the survives-updates guarantee are identical to the ADR agent's, described
[above](#change-the-shape-of-your-adrs). Sections you delete stay deleted.

The shipped template has **no self-certification checklist** on purpose: an agent cannot honestly tick "I
have self-reviewed the full diff". If your override adds one, the command leaves those boxes unchecked and
tells you it left them for you.

One thing the template does *not* control: whether the PR is linked to the issue you passed. Trim the
**Related Issues** section and the command appends a short one rather than dropping the link — saying that it
did. Keep the section if you would rather choose where it sits.

**GitHub only** in this version (via the `gh` CLI), and `gh` is required at run time rather than
optional: without it the command stops with the remedy instead of half-running. Failures *after* that
gate — a protected base branch, a token without push permission, a fork restriction — degrade to the
manual `git push` + `gh pr create` commands (including the base branch it derived) plus an explicit
statement of whether the branch already reached the remote.

## How it works

When you accept the hook's offer (or run it directly) it:

1. **Gates on `gh` first**, stopping before anything else if it is missing or unauthenticated.
2. Confirms the remote is on GitHub. A missing remote, or one on another host, stops with a scope
   statement rather than a `gh` fallback that could not work.
3. Checks the branch, refusing only a detached HEAD and a branch that is already the base.
4. Detects an **existing open PR** and returns its link instead of opening a duplicate.
5. Determines the **base branch**. A promotion flow documented in the constitution's *Version Control &
   Branching Strategy* section or `.specify/extensions/git/git-config.yml` is used and cited. With nothing
   documented it proposes one — the branch yours appears to be cut from, else the repository default.
6. **Offers to commit and push** when the working tree is dirty. Clean tree, unpushed commits — it asks
   to push.
7. **Asks for a linked issue** if you did not pass `--issue`, and accepts a skip.
8. **Resolves the PR template**, fills it from the real diff, and reports which template it used.
9. **Asks once, with everything on the table**: source → base and where the base came from, the issue or
   nothing, draft or ready, the template path, and anything it has already done. Nothing is created
   before you say yes.
10. Opens the PR with `gh` and returns the URL.

Its mutations are the Git and remote actions needed to open the PR — including a commit **when you ask for
one** — and nothing else: never your source, spec, plan, tasks, or constitution.
