# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""Load `agents/`, the only source of truth for agent information.

**Maintainer tooling. Not shipped.** `tools/generate_agent_docs.py` renders every agent output from
what this module loads.

One Markdown file per agent, named by its id, opening with a flat header::

    ---
    id: adr
    title: Architecture Decision Records (ADR)
    ...
    ---

and, for an agent Spectra ships, a long description. `agents/_phases.md` holds the lifecycle phases
as a run of such headers, in order. The header is parsed by hand — the repository supports Python
3.9, so there is no `tomllib`, and the zero-dependency rule rules out YAML — and values are literal:
everything after the first `": "`, so a summary may carry colons, quotes and dashes untouched.

Every problem is reported with the file and, where one applies, the line, and every problem in the
directory is reported at once rather than one per run.
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown_subset as md

PHASES_FILE = "_phases.md"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADER_LINE = re.compile(r"^([a-z]+): (.*)$")

AGENT_KEYS = ("id", "title", "command", "provider", "type", "phase", "order", "status", "summary",
              "manifest")
REQUIRED = ("id", "title", "provider", "type", "phase", "order", "status", "summary")
PHASE_KEYS = ("id", "title", "aidlc")
ENUMS = {
    "provider": ("speckit", "spectra"),
    "type": ("core", "add-on"),
    "status": ("available", "planned"),
}
REQUIRED_ITEMS = ("Arguments", "Use it when")
EXAMPLES = "Examples"


class SourceError(Exception):
    """One or more problems in `agents/`. `problems` lists each, already prefixed with its location."""

    def __init__(self, problems):
        super().__init__("\n".join(problems))
        self.problems = list(problems)


class Phase:
    def __init__(self, fields):
        self.id = fields["id"]
        self.title = fields["title"]
        self.aidlc = fields["aidlc"]


class Section:
    """A `##` section of a body: an item (up to and including Examples) or a guide (after it)."""

    def __init__(self, label, lines, line):
        self.label = label
        self.lines = lines          # content, blank edges trimmed, as written
        self.line = line            # source line of the `##` heading
        self.content_line = line + 1  # corrected to the first non-blank content line on load

    @property
    def joiner(self):
        """`**Label.** text` when the label is a sentence, `**Label** — text` otherwise."""
        return " " if self.label.endswith((".", "?", "!")) else " — "


class Body:
    def __init__(self, lead, lead_line, further, further_line, items, guides):
        self.lead = lead                    # list of lines
        self.lead_line = lead_line
        self.further = further              # list of lines, possibly empty
        self.further_line = further_line
        self.items = items                  # [Section], Arguments first, Examples last
        self.guides = guides                # [Section]

    def item(self, label):
        for section in self.items:
            if section.label == label:
                return section
        raise KeyError(label)

    @property
    def examples(self):
        """The example invocations, one per non-empty line of the Examples fence."""
        code = md.parse(self.item(EXAMPLES).lines)[0]
        return [line for line in code.lines if line.strip()]


class Agent:
    def __init__(self, fields, body, path):
        self.id = fields["id"]
        self.title = fields["title"]
        self.command = fields.get("command")
        self.provider = fields["provider"]
        self.type = fields["type"]
        self.phase = fields["phase"]
        self.order = int(fields["order"])
        self.status = fields["status"]
        self.summary = fields["summary"]
        self.manifest = fields.get("manifest")
        self.body = body
        self.path = path
        self.number = None

    @property
    def shipped(self):
        return self.provider == "spectra" and self.status == "available"

    def roster_entry(self):
        """This agent as an `agents-list.json` entry, keys in the published order."""
        entry = {
            "id": self.id,
            "title": self.title,
            "description": self.summary,
            "status": self.status,
            "phase": self.phase,
            "type": self.type,
            "provider": self.provider,
        }
        if self.command:
            entry["command"] = self.command
        return entry


class Source:
    def __init__(self, phases, agents):
        self.phases = phases
        self.agents = agents

    def shipped(self):
        return [agent for agent in self.agents if agent.shipped]

    def phase(self, phase_id):
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        raise KeyError(phase_id)


# --------------------------------------------------------------------------- #
# Headers
# --------------------------------------------------------------------------- #

def _read_header(lines, start, name, problems):
    """Parse one `---` … `---` block starting at index `start`. Returns (fields, next_index)."""
    if start >= len(lines) or lines[start] != "---":
        problems.append(f"{name}:{start + 1}: expected a header opening with `---`.")
        return None, len(lines)
    fields, lines_of = {}, {}
    i = start + 1
    while i < len(lines) and lines[i] != "---":
        number = i + 1
        match = HEADER_LINE.match(lines[i])
        if not match:
            problems.append(f"{name}:{number}: header lines must be `key: value` "
                            f"(found {lines[i]!r}).")
        else:
            key, value = match.group(1), match.group(2).strip()
            if key in fields:
                problems.append(f"{name}:{number}: `{key}` appears twice in the header.")
            elif not value:
                problems.append(f"{name}:{number}: `{key}` has no value.")
            else:
                fields[key] = value
                lines_of[key] = number
        i += 1
    if i == len(lines):
        problems.append(f"{name}:{start + 1}: the header is never closed with `---`.")
        return None, len(lines)
    fields["_lines"] = lines_of
    fields["_header_line"] = start + 1
    return fields, i + 1


def _load_phases(path, problems):
    name = f"agents/{path.name}"
    lines = path.read_text(encoding="utf-8").split("\n")
    phases, i, seen = [], 0, set()
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        fields, i = _read_header(lines, i, name, problems)
        if fields is None:
            break
        where = f"{name}:{fields['_header_line']}"
        keys = set(fields) - {"_lines", "_header_line"}
        for key in sorted(keys - set(PHASE_KEYS)):
            problems.append(f"{name}:{fields['_lines'][key]}: unknown phase field `{key}`.")
        missing = [key for key in PHASE_KEYS if key not in keys]
        if missing:
            problems.append(f"{where}: phase is missing {', '.join(f'`{k}`' for k in missing)}.")
            continue
        if not SLUG.match(fields["id"]):
            problems.append(f"{name}:{fields['_lines']['id']}: phase id {fields['id']!r} is not a "
                            "lowercase slug.")
        if fields["id"] in seen:
            problems.append(f"{name}:{fields['_lines']['id']}: phase {fields['id']!r} is defined "
                            "twice.")
        seen.add(fields["id"])
        phases.append(Phase(fields))
    if not phases:
        problems.append(f"{name}: defines no phases.")
    return phases


# --------------------------------------------------------------------------- #
# Bodies
# --------------------------------------------------------------------------- #

def _trim(numbered):
    while numbered and not numbered[0][1].strip():
        numbered = numbered[1:]
    while numbered and not numbered[-1][1].strip():
        numbered = numbered[:-1]
    return numbered


def _check_blocks(name, numbered, problems):
    """Parse and render a fragment purely to surface subset violations with their line."""
    if not numbered:
        return []
    try:
        blocks = md.parse([text for _, text in numbered], numbered[0][0])
        md.to_html(blocks)
        return blocks
    except md.MarkdownError as exc:
        problems.append(f"{name}:{exc.line or numbered[0][0]}: {exc}")
        return None


def _split_body(name, numbered, problems):
    """Divide a shipped agent's body into lead, further prose, items and guides, validating each."""
    preamble, sections, current = [], [], None
    in_fence = False
    for number, text in numbered:
        if text.startswith("```"):
            in_fence = not in_fence
        if not in_fence and text.startswith("## "):
            current = (text[3:].strip(), number, [])
            sections.append(current)
            continue
        if not in_fence and text.startswith("#"):
            problems.append(f"{name}:{number}: only `## ` headings are allowed in a body.")
            continue
        (current[2] if current else preamble).append((number, text))

    preamble = _trim(preamble)
    if not preamble:
        problems.append(f"{name}: a shipped agent's body must open with a lead paragraph.")
        return None
    lead = []
    for number, text in preamble:
        if not text.strip():
            break
        lead.append((number, text))
    further = _trim(preamble[len(lead):])
    lead_blocks = _check_blocks(name, lead, problems)
    if lead_blocks is not None and (len(lead_blocks) != 1
                                    or not isinstance(lead_blocks[0], md.Paragraph)):
        problems.append(f"{name}:{lead[0][0]}: the lead must be a single plain paragraph.")
    _check_blocks(name, further, problems)

    labels = [label for label, _, _ in sections]
    if EXAMPLES not in labels:
        problems.append(f"{name}: missing required section \"{EXAMPLES}\".")
        return None
    split = labels.index(EXAMPLES) + 1
    items = [Section(label, [t for _, t in _trim(body)], line)
             for label, line, body in sections[:split]]
    guides = [Section(label, [t for _, t in _trim(body)], line)
              for label, line, body in sections[split:]]

    for position, required in enumerate(REQUIRED_ITEMS):
        if required not in labels[:split]:
            problems.append(f"{name}: missing required section \"{required}\".")
        elif labels[position] != required:
            problems.append(f"{name}:{sections[labels.index(required)][1]}: \"{required}\" must be "
                            f"section {position + 1}.")
    for label in sorted({label for label in labels if labels.count(label) > 1}):
        problems.append(f"{name}: section \"{label}\" appears more than once.")

    for label, line, body in sections:
        trimmed = _trim(body)
        if not trimmed:
            problems.append(f"{name}:{line}: section \"{label}\" is empty.")
            continue
        try:
            md.check_inline(label, line)
        except md.MarkdownError as exc:
            problems.append(f"{name}:{line}: {exc}")
        blocks = _check_blocks(name, trimmed, problems)
        if blocks is None:
            continue
        if label == "Arguments" and not (
                isinstance(blocks[0], md.Paragraph)
                and (len(blocks) == 1 or (len(blocks) == 2 and isinstance(blocks[1], md.ListBlock)))):
            problems.append(f"{name}:{line}: \"Arguments\" must be one paragraph, optionally "
                            "followed by one list.")
        if label == EXAMPLES and (len(blocks) != 1 or not isinstance(blocks[0], md.Code)
                                  or not any(t.strip() for t in blocks[0].lines)):
            problems.append(f"{name}:{line}: \"{EXAMPLES}\" must be exactly one fenced code block "
                            "with one invocation per line.")

    for section, (_, line, body) in zip(items + guides, sections):
        trimmed = _trim(body)
        section.content_line = trimmed[0][0] if trimmed else line + 1

    return Body([t for _, t in lead], lead[0][0], [t for _, t in further],
                further[0][0] if further else None, items, guides)


# --------------------------------------------------------------------------- #
# Agents
# --------------------------------------------------------------------------- #

def _load_agent(path, phase_ids, problems):
    name = f"agents/{path.name}"
    lines = path.read_text(encoding="utf-8").split("\n")
    fields, rest = _read_header(lines, 0, name, problems)
    if fields is None:
        return None
    where = f"{name}:{fields['_header_line']}"
    at = fields["_lines"]
    keys = set(fields) - {"_lines", "_header_line"}
    count = len(problems)

    for key in sorted(keys - set(AGENT_KEYS)):
        problems.append(f"{name}:{at[key]}: unknown field `{key}`.")
    for key in REQUIRED:
        if key not in keys:
            problems.append(f"{where}: missing required field `{key}`.")
    if len(problems) > count:
        return None

    if fields["id"] != path.stem:
        problems.append(f"{name}:{at['id']}: id {fields['id']!r} does not match the file name.")
    for key, allowed in ENUMS.items():
        if fields[key] not in allowed:
            problems.append(f"{name}:{at[key]}: `{key}` must be one of {', '.join(allowed)} "
                            f"(found {fields[key]!r}).")
    if fields["phase"] not in phase_ids:
        problems.append(f"{name}:{at['phase']}: unknown phase {fields['phase']!r}; phases are "
                        f"defined in agents/{PHASES_FILE}.")
    if not fields["order"].isdigit() or int(fields["order"]) < 1:
        problems.append(f"{name}:{at['order']}: `order` must be a positive integer.")
    if len(problems) > count:
        return None

    # The CLI's roster parser rejects these too, but it can only name the agent, not the file and line.
    if fields["status"] == "planned" and "command" in keys:
        problems.append(f"{name}:{at['command']}: a planned agent records no command.")
    elif fields["status"] == "available" and "command" not in keys:
        problems.append(f"{where}: an available agent needs a `command`.")

    shipped = fields["provider"] == "spectra" and fields["status"] == "available"
    if shipped:
        if "manifest" not in keys:
            problems.append(f"{where}: a shipped Spectra agent needs a `manifest` description.")
        expected = f"speckit.spectra.{fields['id']}"
        if fields.get("command") != expected:
            problems.append(f"{name}:{at.get('command', fields['_header_line'])}: a shipped Spectra "
                            f"agent's command must be {expected!r}.")
    elif "manifest" in keys:
        problems.append(f"{name}:{at['manifest']}: only a shipped Spectra agent has a `manifest` "
                        "description.")

    numbered = _trim([(rest + offset + 1, text) for offset, text in enumerate(lines[rest:])])
    body = None
    if shipped:
        if not numbered:
            problems.append(f"{name}: a shipped Spectra agent needs a long description after its "
                            "header.")
        else:
            body = _split_body(name, numbered, problems)
    elif numbered:
        problems.append(f"{name}:{numbered[0][0]}: only a shipped Spectra agent has a body; "
                        "planned and Spec Kit core agents are header-only.")
    if len(problems) > count:
        return None
    return Agent(fields, body, path)


def load(directory):
    """Load and validate `agents/`. Returns a `Source`; raises `SourceError` listing every problem."""
    directory = Path(directory)
    problems = []
    if not directory.is_dir():
        raise SourceError([f"{directory.name}/: the agent source directory does not exist."])

    phases_path = directory / PHASES_FILE
    phases = _load_phases(phases_path, problems) if phases_path.is_file() else []
    if not phases_path.is_file():
        problems.append(f"agents/{PHASES_FILE}: missing.")
    phase_ids = [phase.id for phase in phases]

    agents = []
    for path in sorted(directory.iterdir()):
        if path.name == PHASES_FILE:
            continue
        if path.is_dir() or path.suffix != ".md" or not SLUG.match(path.stem):
            problems.append(f"agents/{path.name}: not an agent file; agents/ holds only "
                            f"<id>.md files and {PHASES_FILE}.")
            continue
        agent = _load_agent(path, phase_ids, problems)
        if agent is not None:
            agents.append(agent)

    positions = {}
    for agent in agents:
        key = (agent.phase, agent.order)
        if key in positions:
            problems.append(f"agents/{agent.path.name}: order {agent.order} in phase "
                            f"{agent.phase!r} is already taken by {positions[key]!r}.")
        positions[key] = agent.id

    if problems:
        raise SourceError(problems)

    agents.sort(key=lambda agent: (phase_ids.index(agent.phase), agent.order))
    for number, agent in enumerate((a for a in agents if a.shipped), start=1):
        agent.number = number
    return Source(phases, agents)
