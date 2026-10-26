#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""Render every agent output from `agents/`, the only source of truth for agent information.

**Maintainer tooling. Not shipped.** `pyproject.toml` lists its packages explicitly
(`packages = ["spectra_cli"]`), so nothing under `tools/` reaches a user's machine, and the shipped
CLI gains no dependency from anything here.

Run it after editing anything under `agents/`::

    python3 tools/generate_agent_docs.py            # rewrite every output
    python3 tools/generate_agent_docs.py --check    # verify without writing (what CI runs)

Each agent is one file, `agents/<id>.md` — a flat header of facts and, for an agent Spectra ships, its
long description — and the phases live in `agents/_phases.md` (see `tools/agent_source.py`). From that
source this script writes, and `--check` verifies (constitution Principle V):

- `agents-list.json`, whole — the published roster that installed CLIs and `docs/agents.html` read at
  run time, byte-for-byte in the shape they have always read;
- marked regions: the Agents table and every agent section of `AGENTS_LIST.md`, the Commands table
  and per-agent sections of `spectra/README.md`, and the sidebar and cards of
  `docs/getting-started/agents.html`;
- named lines: each Spectra command's `description:` in `spectra/extension.yml` and in its command
  file's front matter, both from the same manifest description.

Prose is written by a person, once, in `agents/`. The two long-form outputs carry identical text for
each agent and differ only in framing. A stale output and a hand-edited one fail `--check` the same
way: the output differs from what the source renders.

The built roster is passed through :mod:`spectra_cli.roster`, the parser the CLI itself uses, before
anything is written, so the generator can never publish a roster the CLI would reject. The dependency
runs tools -> package, never the reverse.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_source  # noqa: E402
import markdown_subset as md  # noqa: E402
from spectra_cli import roster as roster_module  # noqa: E402

SCHEMA_VERSION = "1.0"

# Hand-written documentation wraps at 100 columns; generated tables and lists match so the diff
# between a hand-maintained listing and its generated replacement is about content, not reflow.
# Prose is never rewrapped: it keeps the line breaks its author gave it in `agents/`.
WRAP = 100

START_MARKER = "<!-- SPECTRA:GENERATED START id={region} -->"
END_MARKER = "<!-- SPECTRA:GENERATED END id={region} -->"
NOTICE = ("<!-- Generated from agents/ — do not edit by hand. "
          "Run: python3 tools/generate_agent_docs.py -->")

MANIFEST_COMMAND = re.compile(r'^    - name: "(speckit\.spectra\.[^"]+)"$', re.M)
COMMAND_MENTION = re.compile(r"(?:speckit\.spectra\.|/speckit-spectra-)([a-z0-9]+(?:-[a-z0-9]+)*)")

TYPE_LABELS = {"core": "Core", "add-on": "Add-on"}
STATUS_LABELS = {"available": "✅ available", "planned": "🚧 under dev"}


class GeneratorError(Exception):
    """Something is wrong with a marker, a line target, or a document. Message names the culprit."""


def _paths():
    """Every path the generator touches, resolved against REPO_ROOT at call time (tests move it)."""
    return {
        "agents": REPO_ROOT / "agents",
        "roster": REPO_ROOT / "agents-list.json",
        "manifest": REPO_ROOT / "spectra" / "extension.yml",
        "commands": REPO_ROOT / "spectra" / "commands",
        "docs": REPO_ROOT / "docs",
    }


# --------------------------------------------------------------------------- #
# Structured listings (from the roster built out of agents/)
# --------------------------------------------------------------------------- #

def _claude_trigger(command: str) -> str:
    """`speckit.constitution` -> `/speckit-constitution`, the form Claude registers."""
    return "/" + command.replace(".", "-")


def _wrap(text: str, indent: str = "", subsequent: str = None) -> list:
    """Wrap to WRAP columns deterministically — no platform or locale input."""
    return textwrap.wrap(
        text,
        width=WRAP,
        initial_indent=indent,
        subsequent_indent=subsequent if subsequent is not None else indent,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [indent.rstrip()]


def _github_anchor(heading: str) -> str:
    """The fragment GitHub gives a Markdown heading: lowercased, punctuation and emoji dropped, each
    space a hyphen. Unique headings only — GitHub suffixes repeats, and no agent heading repeats."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def _agent_heading(agent, phase_title: str) -> str:
    """The `AGENTS_LIST.md` heading that describes this agent.

    It mirrors what the section renderers write: a shipped agent and a Spec Kit core agent each have
    their own heading, while a planned agent is a list item under its phase's Roadmap heading.
    """
    if agent.provider == "speckit":
        return f"{agent.title} — `{agent.command}` ✅"
    if agent.available:
        return f"{agent.title} ✅"
    return phase_title


def render_agents_table(roster, source) -> list:
    """The Agents table, plus the sentence naming which available agents are Spec Kit's own.

    Each agent's name links to its section further down the same file.

    That sentence enumerates nine agent titles. It is classification wearing prose clothing, and it
    would drift on the very first roster change while every table around it stayed correct — so the
    region is drawn wide enough to include it.
    """
    aidlc = {phase.id: phase.aidlc for phase in roster.phases}
    titles = {phase.id: phase.title for phase in roster.phases}

    lines = [
        "| Agent | SDLC phase | AI-DLC phase | Type | Status |",
        "| ----- | ---------- | ------------ | ---- | ------ |",
    ]
    for agent in roster.agents:
        lines.append(
            f"| [{agent.title}](#{_github_anchor(_agent_heading(agent, titles[agent.phase]))}) "
            f"| {titles[agent.phase]} | {aidlc[agent.phase]} "
            f"| {TYPE_LABELS[agent.type]} | {STATUS_LABELS[agent.status]} |"
        )

    speckit = [a.title for a in roster.agents if a.provider == "speckit" and a.available]
    sentence = (
        f"The agents marked ✅ that aren't shipped by Spectra ({', '.join(speckit)}) are "
        "Spec Kit's own core commands — Spectra layers on top of them."
    )
    return lines + [""] + _wrap(sentence)


def render_speckit_core(roster, source) -> list:
    """One subsection per Spec Kit-provided agent: title, command, description, how to run it."""
    lines = []
    for agent in roster.agents:
        if agent.provider != "speckit":
            continue
        if lines:
            lines.append("")
        lines.append(f"### {agent.title} — `{agent.command}` ✅")
        lines.append("")
        lines.extend(_wrap(agent.description))
        lines.append("")
        lines.append(f"- **Run it (Claude)** — `{_claude_trigger(agent.command)}`")
    return lines


def render_roadmap(roster, source) -> list:
    """Planned agents, grouped under their phase title, in roster order."""
    lines = []
    for phase, agents in roster.grouped():
        planned = [agent for agent in agents if not agent.available]
        if not planned:
            continue
        if lines:
            lines.append("")
        lines.append(f"### {phase.title}")
        lines.append("")
        for agent in planned:
            entry = f"**{agent.title}** ({TYPE_LABELS[agent.type]}) — {agent.description}"
            lines.extend(_wrap(entry, indent="- ", subsequent="  "))
    return lines


def render_spectra_commands(roster, source) -> list:
    """The extension README's Commands table.

    No Effect column: the source does not model per-agent effect. `spectra/extension.yml` declares
    `effect: read-write` for the extension as a whole, and the prose around this table says so.
    """
    lines = [
        "| Command | What it does |",
        "| ------- | ------------ |",
    ]
    for agent in roster.shipped():
        lines.append(f"| `{agent.command}` | {agent.description} |")
    return lines


# --------------------------------------------------------------------------- #
# Long descriptions — the same text, framed for each output
# --------------------------------------------------------------------------- #

def _examples_label(agent) -> str:
    return "Example (Claude)" if len(agent.body.examples) == 1 else "Examples (Claude)"


def _label(agent, section) -> str:
    return _examples_label(agent) if section.label == agent_source.EXAMPLES else section.label


def _opens_with_paragraph(lines) -> bool:
    first = lines[0]
    return not (first.startswith("```") or first.startswith("|") or md.BULLET.match(first)
                or md.ORDERED.match(first))


def _items_markdown(agent) -> list:
    """The labelled facts as one list: `- **Label** — text`, continuation indented two spaces."""
    out = []
    for section in agent.body.items:
        label = _label(agent, section)
        lines = section.lines
        if _opens_with_paragraph(lines):
            out.append(f"- **{label}**{section.joiner}{lines[0]}")
            rest = lines[1:]
        else:
            out.append(f"- **{label}** —")
            rest = lines
        out.extend(("  " + line) if line.strip() else "" for line in rest)
    return out


def _body_markdown(agent, guide_heading: str) -> list:
    """Further prose, the item list, and the guides: everything after the lead, as Markdown."""
    body = agent.body
    out = []
    if body.further:
        out += [""] + body.further
    out += [""] + _items_markdown(agent)
    for guide in body.guides:
        out += ["", f"{guide_heading} {guide.label}", ""] + guide.lines
    return out


def render_agents_list_shipped(roster, source) -> list:
    """Every shipped agent's section of `AGENTS_LIST.md`, in roster order.

    Each section is preceded by a `SPECTRA:AGENT` anchor keyed to the agent's stable id; tests and
    readers slice the file on it.
    """
    lines = []
    for agent in source.shipped():
        if lines:
            lines.append("")
        lines.append(f"<!-- SPECTRA:AGENT id={agent.id} -->")
        lines.append(f"### {agent.title} ✅")
        lines.append("")
        lead = agent.body.lead
        lines.append(f"**`{agent.command}`** — {lead[0]}")
        lines.extend(lead[1:])
        lines.extend(_body_markdown(agent, "####"))
    return lines


def render_spectra_readme_agents(roster, source) -> list:
    """The extension README's per-agent sections — the same text as `AGENTS_LIST.md`."""
    lines = []
    for agent in source.shipped():
        if lines:
            lines += ["", "---", ""]
        lines.append(f"## `{agent.command}` — {agent.title}")
        lines.append("")
        lines.extend(agent.body.lead)
        lines.extend(_body_markdown(agent, "###"))
    return lines


# --------------------------------------------------------------------------- #
# The Agent reference page
# --------------------------------------------------------------------------- #

def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _section_html(agent, section) -> str:
    blocks = md.parse(section.lines, section.content_line)
    label = f"<b>{md.inline_html(_label(agent, section), section.line)}</b>"
    if blocks and isinstance(blocks[0], md.Paragraph):
        joiner = _esc(section.joiner)
        return (label + joiner + md.inline_html(blocks[0].text, blocks[0].line)
                + md.to_html(blocks[1:]))
    return label + md.to_html(blocks)


def full_reference_html(agent) -> list:
    """The whole long description as block HTML, one top-level block per line."""
    body = agent.body
    parts = ["<p>" + md.inline_html("\n".join(body.lead), body.lead_line) + "</p>"]
    if body.further:
        parts += [md.to_html([block]) for block in md.parse(body.further, body.further_line)]
    items = "".join(f"<li>{_section_html(agent, section)}</li>" for section in body.items)
    parts.append(f'<ul class="items">{items}</ul>')
    for guide in body.guides:
        parts.append(f"<h4>{md.inline_html(guide.label, guide.line)}</h4>")
        parts += [md.to_html([block]) for block in md.parse(guide.lines, guide.content_line)]
    return [part.replace("\n", " ") if not part.startswith(("<pre>", "<pre ")) else part
            for part in parts]


PAGE_INDENT = "        "


def render_agents_page_nav(roster, source) -> list:
    return [
        PAGE_INDENT + f'<a href="#a-{agent.id}"><span class="n">{agent.number:02d}</span><span class="t">'
        f"{_esc(agent.title)}<small>{agent.id}</small></span></a>"
        for agent in source.shipped()
    ]


def render_agents_page_cards(roster, source) -> list:
    """One card per shipped agent (contracts/agents-page-markup.md)."""
    lines = []
    for agent in source.shipped():
        card = []
        body = agent.body
        arguments = body.item("Arguments")
        blocks = md.parse(arguments.lines, arguments.content_line)
        args = (md.inline_html(blocks[0].text, blocks[0].line).replace("\n", " ")
                + md.to_html(blocks[1:]).replace("\n", " "))
        card += [
            f'<li class="agent" id="a-{agent.id}">',
            f'  <header><span class="n">{agent.number:02d}</span><h3>{_esc(agent.title)}</h3>'
            f'<span class="phase">{_esc(source.phase(agent.phase).title)}</span></header>',
            f'  <span class="name">{agent.command}</span>',
            '  <span class="cdesc">'
            + md.inline_html("\n".join(body.lead), body.lead_line).replace("\n", " ") + "</span>",
            f'  <div class="args"><b>Arguments:</b> {args}</div>',
            f'  <span class="lbl">{_examples_label(agent)}</span>',
        ]
        card += [f"  <pre><code>{_esc(example)}</code></pre>" for example in body.examples]
        card += ['  <details class="fullref">',
                  "    <summary>Full reference</summary>",
                  '    <div class="fullref-body">']
        lines += [PAGE_INDENT + line for line in card]
        for part in full_reference_html(agent):
            first, *rest = part.split("\n")
            lines.append(PAGE_INDENT + "      " + first)
            lines.extend(rest)   # inside <pre>: whitespace is content, never indent it
        lines += [PAGE_INDENT + line for line in ("    </div>", "  </details>", "</li>")]
    return lines


# --------------------------------------------------------------------------- #
# Outputs
# --------------------------------------------------------------------------- #

# region id -> (file, renderer, indent). Markdown regions put a blank line after the notice.
REGIONS = {
    "agents-list-table": ("AGENTS_LIST.md", render_agents_table, None),
    "agents-list-shipped": ("AGENTS_LIST.md", render_agents_list_shipped, None),
    "agents-list-speckit-core": ("AGENTS_LIST.md", render_speckit_core, None),
    "agents-list-roadmap": ("AGENTS_LIST.md", render_roadmap, None),
    "spectra-readme-commands": ("spectra/README.md", render_spectra_commands, None),
    "spectra-readme-agents": ("spectra/README.md", render_spectra_readme_agents, None),
    "agents-page-nav": ("docs/getting-started/agents.html", render_agents_page_nav, "        "),
    "agents-page-cards": ("docs/getting-started/agents.html", render_agents_page_cards, "        "),
}


def render_roster_json(source) -> str:
    data = {
        "schema_version": SCHEMA_VERSION,
        "phases": [{"id": p.id, "title": p.title, "aidlc": p.aidlc} for p in source.phases],
        "agents": [agent.roster_entry() for agent in source.agents],
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_roster(source):
    """The roster as the CLI would read it, or raise: nothing is written from a roster it rejects."""
    data = json.loads(render_roster_json(source))
    try:
        return roster_module.parse(data, strict=True)
    except roster_module.RosterError as exc:
        named = re.search(r"agent(?: id)? '([a-z0-9-]+)'", str(exc))
        where = f"agents/{named.group(1)}.md" if named else "agents/"
        raise GeneratorError(f"{where}: the roster it builds is invalid ({exc}).") from exc


def _locate(text: str, region: str, relative_path: str):
    """(start_of_body, end_of_body) for a region, or raise.

    Never guesses a region's extent, never appends a missing marker, and never skips a document it
    cannot parse — silently skipping is how a "successful" run leaves documentation stale.
    """
    start = START_MARKER.format(region=region)
    end = END_MARKER.format(region=region)

    for marker, kind in ((start, "start"), (end, "end")):
        count = text.count(marker)
        if count == 0:
            raise GeneratorError(f"{relative_path}: missing {kind} marker for region {region!r}.")
        if count > 1:
            raise GeneratorError(f"{relative_path}: {kind} marker for region {region!r} appears "
                                 f"{count} times.")

    body_start = text.index(start) + len(start)
    body_end = text.index(end)
    if body_end < body_start:
        raise GeneratorError(f"{relative_path}: end marker for region {region!r} precedes its start "
                             "marker.")
    return body_start, body_end


def _known_region_ids(text: str) -> set:
    return set(re.findall(r"<!--\s*SPECTRA:GENERATED START id=([a-z0-9-]+)\s*-->", text))


def render_region(region: str, roster, source) -> str:
    """The full body of a region, including its do-not-edit notice.

    Line endings are always `\\n`, whatever the platform, so a Windows checkout does not look drifted
    to CI.
    """
    _, renderer, indent = REGIONS[region]
    lines = renderer(roster, source)
    if indent is None:
        return "\n" + NOTICE + "\n\n" + "\n".join(lines) + "\n"
    # HTML renderers indent their own lines (the inside of a <pre> must not be indented), so only
    # the notice and the end marker are placed here.
    return "\n" + indent + NOTICE + "\n" + "\n".join(lines) + "\n" + indent


def _description_line(manifest: str) -> str:
    return 'description: "' + manifest.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _named_lines(source):
    """(relative path, selector pattern, replacement line) for every generator-owned line."""
    targets = []
    for agent in source.shipped():
        targets.append((
            "spectra/extension.yml",
            re.compile(r'^(    - name: "' + re.escape(agent.command) + r'"\n      file: "[^"\n]+"\n)'
                       r'      description: .*$', re.M),
            "      " + _description_line(agent.manifest),
        ))
        targets.append((
            f"spectra/commands/{agent.id}.md",
            re.compile(r"\A(---\n(?:(?!---\n)[^\n]*\n)*?)description: .*$", re.M),
            _description_line(agent.manifest),
        ))
    return targets


def render_outputs(source, roster):
    """{relative path: (original text, rendered text)} for every output, without writing anything."""
    rendered = {}

    def current(relative_path):
        if relative_path not in rendered:
            path = REPO_ROOT / relative_path
            try:
                # Decoded from bytes so a CRLF checkout compares as stale and is rewritten with `\n`;
                # `read_text` would normalize the endings and hide the difference.
                text = path.read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise GeneratorError(f"{relative_path}: could not be read ({exc}).") from exc
            rendered[relative_path] = [text, text.replace("\r\n", "\n")]
        return rendered[relative_path]

    roster_text = render_roster_json(source)
    if (REPO_ROOT / "agents-list.json").exists():
        current("agents-list.json")[1] = roster_text
    else:
        rendered["agents-list.json"] = ["", roster_text]

    for region, (relative_path, _, _) in REGIONS.items():
        entry = current(relative_path)
        unknown = _known_region_ids(entry[0]) - {r for r, (p, _, _) in REGIONS.items()
                                                 if p == relative_path}
        if unknown:
            raise GeneratorError(f"{relative_path}: unknown generated region(s) "
                                 f"{', '.join(sorted(unknown))}.")
        body_start, body_end = _locate(entry[1], region, relative_path)
        entry[1] = entry[1][:body_start] + render_region(region, roster, source) + entry[1][body_end:]

    for relative_path, selector, line in _named_lines(source):
        entry = current(relative_path)
        matches = list(selector.finditer(entry[1]))
        if len(matches) != 1:
            raise GeneratorError(f"{relative_path}: expected exactly one generated description line, "
                                 f"found {len(matches)}.")
        match = matches[0]
        entry[1] = entry[1][:match.start()] + match.group(1) + line + entry[1][match.end():]

    return {path: (old, new) for path, (old, new) in rendered.items()}


# --------------------------------------------------------------------------- #
# Verification
# --------------------------------------------------------------------------- #

def check_manifest_agreement(source) -> list:
    """The shipped sources and the manifest agree on membership, and every command has its file."""
    paths = _paths()
    problems = []
    try:
        text = paths["manifest"].read_text(encoding="utf-8")
    except OSError as exc:
        return [f"spectra/extension.yml: could not be read ({exc})."]

    manifest_commands = set(MANIFEST_COMMAND.findall(text))
    shipped = {agent.command: agent.id for agent in source.shipped()}

    for command in sorted(manifest_commands - set(shipped)):
        problems.append(f"spectra/extension.yml registers {command!r}, which no agents/ file "
                        "declares as a shipped Spectra agent.")
    for command in sorted(set(shipped) - manifest_commands):
        problems.append(f"agents/{shipped[command]}.md declares {command!r}, which "
                        "spectra/extension.yml does not register.")
    for agent in source.shipped():
        if not (paths["commands"] / f"{agent.id}.md").is_file():
            problems.append(f"agents/{agent.id}.md: shipped, but spectra/commands/{agent.id}.md "
                            "does not exist.")
    return problems


def _outside_regions(text: str) -> str:
    return re.sub(r"<!-- SPECTRA:GENERATED START.*?<!-- SPECTRA:GENERATED END id=[a-z0-9-]+ -->",
                  "", text, flags=re.S)


def check_command_mentions(source, outputs) -> list:
    """No page names a Spectra command that agents/ does not ship (FR-024)."""
    shipped = {agent.id for agent in source.shipped()}
    texts = []
    docs = REPO_ROOT / "docs"
    if docs.is_dir():
        for path in sorted(docs.rglob("*")):
            if path.suffix in (".html", ".md") and "packages" not in path.relative_to(docs).parts:
                relative = path.relative_to(REPO_ROOT).as_posix()
                text = (outputs[relative][1] if relative in outputs
                        else path.read_text(encoding="utf-8"))
                texts.append((relative, text))
    for relative in ("README.md", "spectra/README.md"):
        if relative in outputs:
            texts.append((relative, _outside_regions(outputs[relative][1])))
        elif (REPO_ROOT / relative).is_file():
            texts.append((relative, (REPO_ROOT / relative).read_text(encoding="utf-8")))

    problems = []
    for relative, text in texts:
        for name in sorted(set(COMMAND_MENTION.findall(text))):
            if name not in shipped:
                problems.append(f"{relative}: names speckit.spectra.{name}, which agents/ does not "
                                "ship.")
    return problems


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def _report(prefix, problems):
    print(f"{prefix}: {len(problems)} problem(s) found:", file=sys.stderr)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)


def run(check: bool) -> int:
    try:
        source = agent_source.load(_paths()["agents"])
    except agent_source.SourceError as exc:
        _report("error", exc.problems)
        return 1

    # A membership mismatch would otherwise surface as a missing description line, which names the
    # symptom rather than the cause.
    mismatch = check_manifest_agreement(source)
    if mismatch:
        _report("error", mismatch)
        return 1

    try:
        roster = build_roster(source)
        outputs = render_outputs(source, roster)
    except (GeneratorError, md.MarkdownError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    stale = sorted(path for path, (old, new) in outputs.items() if old != new)
    problems = check_command_mentions(source, outputs)

    if check:
        problems = [f"{path}: does not match what agents/ renders. "
                    "Run: python3 tools/generate_agent_docs.py" for path in stale] + problems
        if problems:
            _report("error", problems)
            return 1
        print(f"agents/ ({len(source.agents)} agents, {len(source.shipped())} shipped) matches every "
              f"generated output ({len(outputs)} files); the manifest agrees.")
        return 0

    for relative_path in stale:
        # Written as bytes on purpose. `Path.write_text(newline=...)` only exists on Python 3.10+,
        # and `pyproject.toml` declares a 3.9 floor — but the deeper reason is that bypassing the
        # text layer is a stronger guarantee than asking it for `\n`: `read_text` already normalized
        # any CRLF input, so encoding the result cannot reintroduce a platform-specific ending.
        (REPO_ROOT / relative_path).write_bytes(outputs[relative_path][1].encode("utf-8"))
        print(f"rewrote {relative_path}")
    if not stale:
        print("every generated output was already current")
    if problems:
        _report("warning", problems)
        return 1
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="generate_agent_docs",
        description="Render every agent output from agents/.",
    )
    parser.add_argument("--check", action="store_true",
                        help="verify without writing; exit non-zero on any mismatch")
    args = parser.parse_args(argv)
    return run(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
