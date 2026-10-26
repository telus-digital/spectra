#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""One-off seeding report for feature 040 (task T023, FR-016). Not maintained tooling.

For each shipped agent, reads every copy of its prose as it stood on `main` before `agents/` existed —
the `AGENTS_LIST.md` block, the `spectra/README.md` section, the Agent reference card, and the command
file's own description — splits each into sentences, and lists every sentence that does not appear
verbatim (after normalizing whitespace and markup) in the agent's new source file.

A missing sentence is marked `reworded` when a source sentence is close to it
(`difflib.SequenceMatcher` ratio >= 0.6, quoted as the pointer), otherwise `dropped`. The implementer
may promote a `dropped` entry to `merged` only through NOTES below, naming where the content lives now.

    python3 specs/040-agent-single-source/seed/seed_report.py            # write seeding-report.md
    python3 specs/040-agent-single-source/seed/seed_report.py --summary  # counts only, to stdout
"""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# The last commit before feature 040: the copies the seed was taken from. Pinned, because `main`
# now carries the generated outputs and would compare them with themselves.
BASE = "1e724abfe668e06c90c9ee6c4ff7a2df93d0d3e7"
REPORT = REPO / "specs" / "040-agent-single-source" / "seeding-report.md"
THRESHOLD = 0.6

# (agent id, exact normalized sentence prefix) -> where the content lives now. Filled in by hand.
NOTES = {
    ('test-plan', 'Suggests UAT scenarios — at least one pe'): 'step 6 of ## How it works and the UAT scenarios bullet',
    ('test-plan', 'The run reports the count: criteria cove'): 'step 7 of ## How it works',
    ('test-plan', 'UAT scenarios become a final phase title'): '## Feeding it to the planner is one copy-paste. and ## How it works',
    ('adr', 'Checks the decision against your constit'): 'step 4 of ## How it works and the lead paragraph',
    ('uat', 'Pass --env <name-or-url> to act on an en'): '## Arguments and ## Other environments',
    ('defect-rca', 'An evidence table of nothing but confirm'): "the lead's 'The document records what was ruled out' paragraph and ## How it works",
    ('create-pr', 'Gates on gh first.'): "the lead's gh-gate paragraph",
    ('review-pr', 'Gates on gh first.'): "the lead's gh-gate paragraph",
    ('review-pr', '⏎ ⏎ Optional arguments: ⏎ ⏎ - (none) — o'): 'covered by ## Arguments',
    ('deployment-strategy', 'Reads your project — constitution, specs'): 'the lead paragraph and ## What it reads and records',
    ("domain-analyzer", "A foundation-phase command whose output ex"): "restates the lead paragraph (hand-off to the constitution); the phase is in the header",
    ("domain-analyzer", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("domain-analyzer", "No arguments required — it analyzes the wh"): "covered by ## Arguments",
    ("domain-analyzer", "/speckit-spectra-domain-analyzer focus on "): "usage example; the focus hint is covered by ## Arguments and ## Examples",
    ("methodology", "A foundation-phase command that writes dow"): "restates the lead paragraph (onboarding-grade methodology handed to the constitution)",
    ("methodology", "It is built for an existing codebase bein"): "covered by ## Use it when (existing codebase or a new project)",
    ("methodology", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("kb-vault", "A foundation-phase command that takes kno"): "restates the lead paragraph",
    ("kb-vault", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("test-strategy", "A foundation-phase command that decides h"): "restates the lead paragraph (decide how the project tests itself, once, at the start)",
    ("test-strategy", "The five questions are where the testing "): "restates the lead's second paragraph",
    ("test-strategy", "Every recommendation cites a path in your"): "restates the lead's third paragraph",
    ("test-strategy", "Every coverage figure carries its provena"): "restates the lead's brownfield paragraph (measured/reported/unavailable)",
    ("test-strategy", "UAT and regression are policy, not levels"): "restates the lead ('The last two lenses are policy rather than levels')",
    ("test-strategy", "The lens set and the ownership map are re"): "restates the lead's UAT/regression paragraph",
    ("test-strategy", "It drafts each guardrail under a frozen t"): "restates the lead's 'Two things it will not do' paragraph",
    ("test-strategy", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("brd", "Asks up to 5 clarifying questions, but on"): "restates the lead paragraph (up to five clarifying questions only on material gaps)",
    ("brd", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("brd", "Or point it at a document:"): "covered by ## Examples (the .docx example)",
    ("defect-rca", "Your attention is spent on the runtime f"): "restates the lead paragraph",
    ("defect-rca", "The first two require a citation; undete"): "restates the lead (prior-analysis paragraph)",
    ("defect-rca", "Invalidated hypotheses appear in the doc"): "restates the lead (evidence-table paragraph); also in ## How it works",
    ("defect-rca", "The file is named before the analysis co"): "first clause in ## Where it writes; remainder in ## The document",
    ("defect-rca", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("create-pr", "It runs on demand from any branch, and i"): "restates the lead (works from any branch; offered by the after_implement hook)",
    ("create-pr", "If gh is missing or unauthenticated it s"): "restates the lead's gh-gate paragraph",
    ("create-pr", "Nothing is mutated on that path."): "restates the lead's gh-gate paragraph",
    ("create-pr", "Only two refusals: a detached HEAD, and "): "restates the lead (Works from any branch); step 3 of ## How it works",
    ("create-pr", "A fix/… or chore branch is fine — a spec"): "restates the lead (Works from any branch)",
    ("create-pr", "Say yes and it behaves like an ordinary "): "restates the lead (Uncommitted work paragraph)",
    ("create-pr", "Nothing is created before you say yes — "): "step 9 of ## How it works; redirecting the base is in ## Base branch",
    ("create-pr", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("create-pr", "Optional arguments:"): "a label only; covered by ## Arguments",
    ("review-pr", "Standards form a fixed chain — constitut"): "covered by ## Standards",
    ("review-pr", "Locates the governing spec from the PR's"): "covered by ## Spec discovery (the single question is in ## Linked issue)",
    ("review-pr", "Neither the branch name nor Spec Kit's m"): "covered by ## Spec discovery; the feature.json path is in ## How it works",
    ("review-pr", "Spec Kit keeps that file out of version "): "covered by ## Spec discovery",
    ("review-pr", "Reads the linked issue as optional extra"): "covered by ## Linked issue",
    ("review-pr", "You see the exact review first — body an"): "restates the lead (exact text shown, one review event under your own gh credentials)",
    ("review-pr", "Approving over a blocker you accepted re"): "covered by ## Good to know",
    ("review-pr", "The published body declares that it was "): "restates the lead paragraph",
    ("review-pr", "Prior findings are recovered by reading "): "covered by ## Findings land on the lines they are about; the override is in ## Change the shape of your reviews",
    ("deployment-strategy", "Every lens adapts — for a library, envir"): "restates the lead paragraph (what-ships classification)",
    ("deployment-strategy", "Asks you five things it cannot read — ho"): "restates the lead paragraph (five questions)",
    ("deployment-strategy", "Works six lenses — environments and prom"): "restates the lead paragraph (six lenses)",
    ("deployment-strategy", "Writes one document to docs/DEPLOYMENT_S"): "restates the lead paragraph (output path and Mermaid diagram)",
    ("deployment-strategy", "Checks your constitution, drafts only du"): "restates the lead paragraph; ds- IDs in ## What it reads and records",
    ("deployment-strategy", "Every claim is verified, claimed, stated"): "restates the lead's provenance sentence; convention is defined in ## What it reads and records",
    ("deployment-strategy", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("impact", "A Requirements & Discovery-phase command"): "restates the lead paragraph (runs before specify)",
    ("impact", "Give it one paragraph describing what sh"): "restates the lead paragraph",
    ("impact", "The impact rating is derived from a defi"): "restates the lead's refusal bullets",
    ("impact", "The output never claims absence of impac"): "restates the lead's refusal bullets",
    ("impact", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("impact", "With a supporting document, or unattende"): "covered by ## Examples",
    ("impact", "Analyses land in docs/impact-analysis/ b"): "restates ## Where it writes",
    ("impact", "The command checks whether docs/ is a pu"): "restates ## Where it writes; the secrets detail is in ## Numbering, interruptions, and the publishing check",
    ("impact", "Approval is manual, and stays yours."): "restates ## Approval is yours, and manual.",
    ("test-plan", "Run it after specify and it:"): "a label only; restates the lead paragraph",
    ("test-plan", "A lens the strategy ruled out is unavail"): "restates the 'It honours the whole strategy' bullet",
    ("test-plan", "Traceability runs both ways, and that is"): "restates the lead paragraph",
    ("test-plan", "The test plan and plan.md always land in"): "restates the 'It finds the feature exactly as plan does' bullet",
    ("test-plan", "A path argument only confirms the featur"): "covered by ## Arguments",
    ("test-plan", "It never invents a decision your spec do"): "restates the 'It never invents the missing decision' bullet",
    ("test-plan", "It is approved, not tracked; tasks.md is"): "restates the no-checkboxes bullet",
    ("test-plan", "A coverage claim cites the test file; an"): "restates the 'It runs nothing' bullet",
    ("test-plan", "Unlike the other document agents it writ"): "restates ## Where it writes",
    ("test-plan", "It follows the ownership map when choosi"): "restates the 'It honours the whole strategy' bullet",
    ("test-plan", "The handoff lands in plan.md."): "restates ## Feeding it to the planner is one copy-paste.",
    ("test-plan", "It is offered, never run, after specify."): "restates ## Use it when",
    ("test-plan", "An optional hook asks whether to generat"): "restates ## Use it when",
    ("test-plan", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("test-plan", "No path is needed."): "covered by ## Arguments",
    ("test-plan", "The document's seven sections are overri"): "restates ## Template",
    ("uat", "An optional command that runs after impl"): "restates the lead paragraph",
    ("uat", "The implement command leaves the UAT pha"): "restates the lead paragraph",
    ("uat", "A tick is a claim that acceptance happen"): "restates the 'It ticks only what it saw pass' paragraph",
    ("uat", "The hook only asks."): "restates ## Use it when",
    ("uat", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("uat", "No path is needed; a path to the feature"): "covered by ## Arguments",
    ("flaky-test-detector", "It finds the tests that pass and fail on"): "restates the lead paragraph and the 'Two gates' paragraph",
    ("flaky-test-detector", "Detection is a read of the source, which"): "restates the lead paragraph",
    ("flaky-test-detector", "Deleting an assertion, loosening one so "): "restates the 'A fix removes the cause' paragraph",
    ("flaky-test-detector", "Usage (Claude):"): "a label only; usage is covered by ## Examples",
    ("flaky-test-detector", "Or narrow it to one part of a monorepo:"): "covered by ## Examples and ## Arguments",
}


def _drop_marker_lines(block):
    """Blank each whole-line marker comment and `###` heading, keeping the line count."""
    return "\n".join("" if (line.startswith("<!--") and line.endswith("-->")) or line.startswith("### ")
                     else line for line in block.split("\n"))


def old(path):
    return subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=REPO, check=True,
                          capture_output=True, text=True).stdout


def normalize(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*`]", "", text)
    text = re.sub(r"^\s*(?:[-|]|\d+\.)\s*", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def sentences(text):
    text = re.sub(r"```.*?```", lambda m: "\n" + m.group(0).replace("\n", " ⏎ ") + "\n", text,
                  flags=re.S)
    pieces = []
    for chunk in re.split(r"\n\s*\n|\n(?=\s*(?:[-|]|\d+\.) )|\n(?=#)", text):
        chunk = normalize(chunk)
        pieces += [p for p in re.split(r"(?<=[.!?:])\s+(?=[A-Z0-9(\"“/])", chunk) if p]
    return [p for p in pieces if len(p) > 3 and not re.fullmatch(r"[#\s—-]*", p)]


def copies(agent_id, command):
    al = old("AGENTS_LIST.md")
    start = al.index(f"<!-- SPECTRA:AGENT id={agent_id} -->")
    nxt = al.find("<!-- SPECTRA:AGENT id=", start + 1)
    block = al[start:nxt if nxt != -1 else al.index("## Spec Kit core agents")]
    block = _drop_marker_lines(block)

    readme = old("spectra/README.md")
    start = readme.index(f"## `{command}`")
    section = readme[start:readme.index("\n## ", start + 1)]
    section = section.split("\n", 1)[1]

    page = old("docs/getting-started/agents.html")
    start = page.index(f'<span class="name">{command}</span>')
    card = page[start:page.index("</li>", start)]
    card = re.sub(r"<pre>.*?</pre>", "", card, flags=re.S).replace(command, "")
    card = html.unescape(re.sub(r"<[^>]+>", "", card))

    front = old(f"spectra/commands/{agent_id}.md").split("---")[1]
    description = re.search(r'^description: "(.*)"$', front, re.M).group(1)

    return [("AGENTS_LIST.md", block), ("spectra/README.md", section),
            ("docs/getting-started/agents.html (card)", card),
            (f"spectra/commands/{agent_id}.md (description)", description)]


def rendered_copies(agent):
    text = (REPO / "AGENTS_LIST.md").read_text(encoding="utf-8")
    start = text.index(f"<!-- SPECTRA:AGENT id={agent.id} -->")
    nxt = text.find("<!-- SPECTRA:AGENT id=", start + 1)
    block = text[start:nxt if nxt != -1 else text.index("<!-- SPECTRA:GENERATED END", start)]
    return _drop_marker_lines(block)


def main():
    sys.path.insert(0, str(REPO / "tools"))
    import agent_source  # noqa: E402

    source = agent_source.load(REPO / "agents")
    out = ["# Seeding report — feature 040", "",
           ("Every sentence from a pre-040 copy of an agent's prose that does not appear verbatim in "
            "its new `agents/<id>.md` (FR-016). `reworded` quotes the closest source sentence; "
            "`dropped` had none close; `merged` names where the content went. Generated by "
            "`seed/seed_report.py`."), ""]
    summary = []
    for agent in source.shipped():
        # Compare against what the source renders, so an item's `**Label** —` framing matches.
        rendered = rendered_copies(agent)
        candidates = sentences(rendered)
        target = " ".join(candidates)
        entries = []
        for name, copy in copies(agent.id, agent.command):
            missing = []
            for sentence in sentences(copy):
                if sentence in target:
                    continue
                note = next((v for (aid, prefix), v in NOTES.items()
                             if aid == agent.id and sentence.startswith(prefix)), None)
                if note:
                    missing.append(("merged", sentence, note))
                    continue
                best = max(candidates, key=lambda c: difflib.SequenceMatcher(None, sentence, c)
                           .ratio(), default="")
                ratio = difflib.SequenceMatcher(None, sentence, best).ratio()
                missing.append(("reworded", sentence, best) if ratio >= THRESHOLD
                               else ("dropped", sentence, None))
            entries.append((name, missing))
        summary.append((agent.id, [(name, len(m)) for name, m in entries]))
        out += [f"## {agent.id}", ""]
        for name, missing in entries:
            out.append(f"### {name} — {len(missing)} sentence(s) not carried verbatim")
            out.append("")
            for mark, sentence, pointer in missing:
                out.append(f"- **{mark}** — {sentence}")
                if pointer:
                    out.append(f"  - → {pointer}")
            if missing:
                out.append("")
            else:
                out += ["Everything carried over verbatim.", ""]

    if "--summary" in sys.argv:
        for agent_id, counts in summary:
            print(agent_id, ", ".join(f"{name.split(' ')[0]}={n}" for name, n in counts))
        return
    REPORT.write_bytes(("\n".join(out).rstrip() + "\n").encode("utf-8"))
    print(f"wrote {REPORT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
