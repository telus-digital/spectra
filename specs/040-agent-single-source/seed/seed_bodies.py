#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""One-off seeding for feature 040 (tasks T014–T017, first pass). Not maintained tooling.

Converts each shipped agent's block of the pre-040 `AGENTS_LIST.md` into the body format of
`agents/<id>.md`: the lead without its bold command prefix, the further prose as written, and each
`- **Label** — text` item as a `## Label` section. Material that existed only in `spectra/README.md`
is merged by hand afterwards, as guides after `## Examples`; `seed_report.py` accounts for every
sentence that did not carry over.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# The last commit before feature 040: the copies the seed was taken from. Pinned, because `main`
# now carries the generated outputs and would compare them with themselves.
BASE = "1e724abfe668e06c90c9ee6c4ff7a2df93d0d3e7"
ITEM = re.compile(r"^- \*\*(.+?)\*\*( —(?: |(?=$))|\s|$)(.*)$")


def old(path):
    return subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=REPO, check=True,
                          capture_output=True, text=True).stdout


def blocks():
    text = old("AGENTS_LIST.md")
    ids = re.findall(r"<!-- SPECTRA:AGENT id=([a-z0-9-]+) -->", text)
    for agent_id in ids:
        start = text.index(f"<!-- SPECTRA:AGENT id={agent_id} -->")
        nxt = text.find("<!-- SPECTRA:AGENT id=", start + 1)
        end = nxt if nxt != -1 else text.index("## Spec Kit core agents")
        yield agent_id, text[start:end].rstrip().rstrip("-").rstrip().split("\n")[2:]


def convert(agent_id, lines):
    while lines and not lines[0].strip():
        lines = lines[1:]
    prefix = f"**`speckit.spectra.{agent_id}`** — "
    assert lines[0].startswith(prefix), (agent_id, lines[0])
    lines[0] = lines[0][len(prefix):]
    first_item = next(i for i, line in enumerate(lines) if line.startswith("- **Arguments**"))
    out = [line for line in lines[:first_item]]
    while out and not out[-1].strip():
        out.pop()

    notes = []
    for line in lines[first_item:]:
        match = ITEM.match(line)
        if match:
            label, joiner, rest = match.groups()
            if label.startswith("Example"):
                label = "Examples"
            elif joiner.strip() != "—" and not label.endswith((".", "?", "!")):
                notes.append(f"{agent_id}: item {label!r} is part of a sentence; reworded")
                rest = f"{label} {rest}".strip()
                label = "What it does not do" if label == "It does not" else label
            out += ["", f"## {label}", ""]
            if rest:
                out.append(rest)
        elif line.startswith("  ") or not line.strip():
            out.append(line[2:] if line.startswith("  ") else "")
        else:
            raise SystemExit(f"{agent_id}: unexpected line in the item list: {line!r}")
    while out and not out[-1].strip():
        out.pop()
    return _use_it_when_second(agent_id, out, notes), notes


def _use_it_when_second(agent_id, out, notes):
    """FR-004 fixes the order Arguments, Use it when; two blocks had other items in between."""
    heads = [i for i, line in enumerate(out) if line.startswith("## ")]
    labels = [out[i][3:] for i in heads]
    if labels.index("Use it when") == 1:
        return out
    notes.append(f"{agent_id}: moved 'Use it when' to follow 'Arguments'")
    sections = {}
    for n, start in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(out)
        sections[labels[n]] = out[start:end]
    order = ["Arguments", "Use it when"] + [l for l in labels if l not in ("Arguments", "Use it when")]
    rebuilt = out[:heads[0]]
    for label in order:
        chunk = sections[label]
        while chunk and not chunk[-1].strip():
            chunk = chunk[:-1]
        rebuilt += chunk + [""]
    return rebuilt[:-1]


def main():
    for agent_id, lines in blocks():
        body, notes = convert(agent_id, lines)
        path = REPO / "agents" / f"{agent_id}.md"
        header = path.read_text(encoding="utf-8").split("---\n")[1]
        path.write_bytes(("---\n" + header + "---\n\n" + "\n".join(body) + "\n").encode("utf-8"))
        for note in notes:
            print(note)


if __name__ == "__main__" and "--merge" not in __import__("sys").argv:
    main()


# --------------------------------------------------------------------------- #
# Second pass: merge material that only spectra/README.md carried, as guides after Examples.
# --------------------------------------------------------------------------- #

KEEP_INTRO = {}
COVERED = 0.8      # a chunk whose sentences are this much present in the base is a restatement
CLOSE = 0.85       # a sentence this similar to a base sentence counts as present


def _readme_section(command):
    text = old("spectra/README.md")
    start = text.index(f"## `{command}`")
    section = text[start:text.index("\n## ", start + 1)].split("\n")[1:]
    while section and section[-1].strip() in ("", "---"):
        section.pop()
    return section


def _chunks(lines):
    """Blank-line separated chunks, keeping fences whole and gluing a `…:` lead-in to what follows."""
    chunks, current, in_fence = [], [], False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        if not line.strip() and not in_fence:
            if current:
                chunks.append(current)
                current = []
            continue
        current.append(line)
    if current:
        chunks.append(current)
    glued = []
    for chunk in chunks:
        if glued and glued[-1][-1].rstrip().endswith(":"):
            glued[-1] = glued[-1] + [""] + chunk
        else:
            glued.append(chunk)
    return glued


def _covered(chunk, base_sentences, base_text):
    import difflib
    sys_path = str(REPO / "specs" / "040-agent-single-source" / "seed")
    import sys
    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    from seed_report import sentences  # noqa: E402
    found = sentences("\n".join(chunk))
    if not found:
        return 1.0
    hits = 0
    for sentence in found:
        if sentence in base_text or any(
                difflib.SequenceMatcher(None, sentence, b).ratio() >= CLOSE for b in base_sentences):
            hits += 1
    return hits / len(found)


def merge_readme(agent_id, command, body_lines, dropped):
    import sys
    sys.path.insert(0, str(REPO / "specs" / "040-agent-single-source" / "seed"))
    from seed_report import sentences  # noqa: E402

    base_sentences = sentences("\n".join(body_lines))
    base_text = " ".join(base_sentences)
    examples = set()
    in_examples = False
    for line in body_lines:
        if line == "## Examples":
            in_examples = True
        elif in_examples and line.strip() and not line.startswith("```"):
            examples.add(line.strip())

    section = _readme_section(command)
    parts, title, current, in_fence = [], "How it works", [], False
    for line in section:
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("### "):
            parts.append((title, current))
            title, current = line[4:].strip(), []
            continue
        current.append(line)
    parts.append((title, current))

    guides = []
    for title, lines in parts:
        if title == "How it works" and title not in KEEP_INTRO.get(agent_id, ()):
            # FR-016: only sections that exist only in the README are added. The README's opening
            # paragraphs restate the agent in other words; they are listed in the seeding report.
            continue
        kept = []
        for chunk in _chunks(lines):
            text = "\n".join(chunk)
            fence_lines = [l.strip() for l in chunk if l.strip() and not l.startswith("```")]
            if chunk[0].startswith("```") and set(fence_lines) <= examples:
                dropped.append((agent_id, title, text))
                continue
            if re.fullmatch(r"Usage \(Claude\):", text.strip()):
                dropped.append((agent_id, title, text))
                continue
            if _covered(chunk, base_sentences, base_text) >= COVERED:
                dropped.append((agent_id, title, text))
                continue
            kept.append(chunk)
        if kept:
            guide = [f"## {title}", ""]
            for chunk in kept:
                guide += chunk + [""]
            guides.append(guide[:-1])
    out = list(body_lines)
    for guide in guides:
        out += [""] + guide
    return out


def main_merge():
    dropped = []
    for agent_id, lines in blocks():
        body, _ = convert(agent_id, lines)
        merged = merge_readme(agent_id, f"speckit.spectra.{agent_id}", body, dropped)
        path = REPO / "agents" / f"{agent_id}.md"
        header = path.read_text(encoding="utf-8").split("---\n")[1]
        path.write_bytes(("---\n" + header + "---\n\n" + "\n".join(merged) + "\n").encode("utf-8"))
    for agent_id, title, text in dropped:
        print(f"--- dropped as restatement: {agent_id} / {title}")
        print(text)


if __name__ == "__main__" and "--merge" in __import__("sys").argv:
    main_merge()
