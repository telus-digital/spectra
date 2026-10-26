# Feature Specification: One Source of Truth for Every Agent

**Feature Branch**: `040-agent-single-source`

**Created**: 2026-10-25

**Status**: Implemented

**Input**: User description: "Make an agents/ directory the single source of truth for everything about an agent. One Markdown file per agent: a strict flat key: value header (id, title, command, provider, type, phase, status, summary, manifest) parsed with the standard library, and a Markdown body holding the long description (lead paragraph, further paragraphs, then Arguments, Use it when, and Examples sections); planned agents have a header only; phases live in agents/_phases.md. tools/generate_agent_docs.py renders every agent listing from it: agents-list.json (same schema as today, so installed CLIs and docs/agents.html keep working, now a committed build output rather than hand-edited), the README and spectra/README.md tables and per-agent sections, every section of AGENTS_LIST.md, the extension.yml command descriptions, and the sidebar and cards of docs/getting-started/agents.html (lead paragraph, Arguments, Examples, and a Full reference link), converting the Markdown subset in use to HTML. --check fails when any output is out of date with the source. Seed the long descriptions from AGENTS_LIST.md. Pages stay static apart from docs/agents.html's existing fetch of agents-list.json."

## Background

Everything a reader can learn about a Spectra agent is written today in up to six places, by hand,
and the copies have drifted apart:

| Where | What it says about each agent | How it is kept |
| --- | --- | --- |
| `agents-list.json` | title, phase, type, status, provider, command, one-line description | hand-edited |
| `AGENTS_LIST.md` | the full write-up for every shipped agent | hand-written prose, existence checked |
| `spectra/README.md` | a long per-agent user guide, shipped inside the package | hand-written |
| `docs/getting-started/agents.html` | a one-paragraph card, arguments, and an example | hand-written |
| `spectra/extension.yml` | the description Spec Kit shows in the user's agent | hand-written |
| `spectra/commands/*.md` | a front-matter description of its own, worded differently again | hand-written |

Structured listings (tables, the roadmap, the core-agent list) are already generated from
`agents-list.json`; the paragraphs are not, and nothing checks that they agree. The ADR agent's card on
the website says it "asks a few clarifying questions" while `AGENTS_LIST.md` says "up to five", for
example. Changing one fact about one agent means finding and editing every copy, and adding an agent
means remembering every place it must appear.

## User Scenarios & Testing *(mandatory)*

The actor throughout is the **maintainer** — the single owner of this repository, who adds agents,
rewords them, and ships the site and the package. The readers of the generated pages benefit
indirectly: they stop seeing different stories about the same agent in different places.

### User Story 1 - Change an agent's description in one place (Priority: P1)

The maintainer rewords what an existing agent does. They edit that agent's one source file, run the
generator, and every page and file that describes the agent — the full reference, the website card,
the roster, the README tables — now says the new thing. They never open those files by hand.

**Why this priority**: Drift between copies is the problem this feature exists to remove. Without
this, nothing else matters.

**Independent Test**: Change one sentence in one agent's source file, run the generator, and confirm
the sentence appears in every output that shows that part of the description and that no other file
changed.

**Acceptance Scenarios**:

1. **Given** a shipped agent's source file, **When** the maintainer changes its lead paragraph and runs
   the generator, **Then** the agent's section in the full reference and its card on the Agent
   reference page both show the new paragraph.
2. **Given** a shipped agent's source file, **When** the maintainer changes its one-line summary and
   runs the generator, **Then** the roster data file, the Agent Roster page (through that data file),
   and every generated listing that shows the summary show the new summary.
3. **Given** the maintainer edited an agent's source file but did not run the generator, **When** the
   check runs (locally or in CI), **Then** it fails and names each output that is out of date.
4. **Given** the maintainer hand-edits an agent's text directly in a generated output, **When** the
   check runs, **Then** it fails and says the text must be changed in the source instead.

---

### User Story 2 - Add a new agent by adding one file (Priority: P1)

The maintainer ships a new agent. They add one source file for it, with its header and its long
description, and run the generator. The agent now appears everywhere it should: the roster data, the
roster page, the README tables, the full reference, and a card in the Agent reference page sidebar, in
its lifecycle position.

**Why this priority**: Adding agents is the most common roster change and the one most likely to miss
a place today.

**Independent Test**: Add a source file for a hypothetical shipped agent, run the generator, and
confirm it appears in every output in the right order; then remove a required part of the file and
confirm the check names what is missing.

**Acceptance Scenarios**:

1. **Given** a new source file for a shipped agent with every required header field and body section,
   **When** the maintainer runs the generator, **Then** the agent appears in every output, numbered
   and ordered by its lifecycle position.
2. **Given** a new source file for a planned agent with a header only, **When** the generator runs,
   **Then** the agent appears in the roster data and the roadmap, and nowhere that needs a long
   description.
3. **Given** a shipped agent's source file missing a required body section (for example Examples),
   **When** the generator or the check runs, **Then** it stops and names the file and the missing
   section.
4. **Given** a shipped agent whose command is not registered in the extension manifest, or a manifest
   command with no source file, **When** the check runs, **Then** it fails and names the mismatch.

---

### User Story 3 - Installed tools and the live site keep working (Priority: P1)

Users who installed the `spectra` command earlier, and the live Agent Roster page, read the roster
data file from the repository at run time. After this change that file is produced by the generator
instead of being edited by hand, but it reads exactly as before, so nobody notices.

**Why this priority**: The roster data file is a published interface. Breaking it breaks every
installed copy of the command and the roster page at once.

**Independent Test**: Generate the roster data file from the seeded source and compare it with the
current hand-edited file: same fields, same values, same order. Run the existing command-line and
roster tests against it unchanged.

**Acceptance Scenarios**:

1. **Given** the source seeded from today's content, **When** the generator writes the roster data
   file, **Then** its content is identical in meaning to the current file: same agents, same order,
   same field names and values, same schema version.
2. **Given** the generated roster data file, **When** an installed `spectra agent-list` reads it,
   **Then** it lists the same agents as it does today.
3. **Given** the generated roster data file, **When** the Agent Roster page loads it, **Then** it shows
   the same agents, groups, and descriptions as today.

---

### User Story 4 - The Agent reference page builds itself (Priority: P2)

The Agent reference page (`docs/getting-started/agents.html`) stops being hand-maintained. Its sidebar
and its cards are generated: each card shows the agent's lead paragraph, its Arguments, its Examples,
and a collapsed "Full reference" section that expands in place to show the agent's full description.
The page stays plain static HTML.

**Why this priority**: This is the page that prompted the change, but stories 1–3 must hold first.

**Independent Test**: Regenerate the page and open it with scripts disabled; every card and sidebar
item is present, every Full reference section expands to that agent's full description, and the
existing tests that read cards from this page pass.

**Acceptance Scenarios**:

1. **Given** the generated page, **When** a reader opens it with scripts disabled, **Then** every
   shipped agent's card and sidebar entry is present.
2. **Given** a card, **When** the reader expands its Full reference section, with scripts disabled,
   **Then** it shows the same text as that agent's section in the full reference, without leaving the
   page.
3. **Given** formatting in the source (bold, italics, inline code, links, code blocks), **When** the
   card is generated, **Then** it renders with the same emphasis as the full reference.
4. **Given** formatting outside the supported subset, **When** the generator runs, **Then** it stops and
   names the file and line rather than producing broken or unescaped HTML.

---

### User Story 5 - The constitution names the source (Priority: P3)

The constitution says the agent source directory is the only source of truth for agent information,
that every listing and every copy of an agent's prose is rendered from it, and that the prose itself
is still written by a person.

**Why this priority**: Needed so the plan's Constitution Check passes and future work does not
reintroduce hand-maintained copies, but it is a governance change rather than a capability.

**Independent Test**: Read Principle V after the amendment; it names the source directory as the only
source of truth and lists every generated output.

**Acceptance Scenarios**:

1. **Given** the amended constitution, **When** a contributor reads Principle V, **Then** it names the
   agent source directory as the sole source of agent information and the roster data file as a
   generated output.

---

### Edge Cases

- **Spec Kit core agents** (constitution, specify, plan, and so on) are not shipped by Spectra and have
  no long description; their source files are header-only and they appear only in outputs that show
  the one-line summary.
- **Two agents share one command** (Testing runs inside `speckit.implement`): the source allows it, and
  outputs keyed by command do not collapse or duplicate them.
- **A header field with a value containing a colon or quotes** (summaries often contain " — " and
  quotes): the header format must carry it without escaping surprises.
- **An unknown header field, a missing required field, a duplicate id, or an unknown phase**: generation
  stops and names the file and field.
- **A source file for an agent whose status is planned but which has a body**: rejected, so roadmap
  text never leaks onto pages meant for shipped agents.
- **A file in the source directory that is not an agent** (for example the phases file, or a stray
  note): only the designated phases file is treated specially; anything else that fails to parse
  stops generation.
- **A rendered output contains text that only existed in that output before this change** (for
  example a template-override walkthrough that only `spectra/README.md` carries): it moves into the
  source per FR-015 and FR-016.
- **A command file's description and its manifest description disagree today**: seeding keeps the
  manifest wording, and the command file's old wording is listed for the maintainer per FR-016.
- **Changing an agent's manifest description changes a shipped file**: the usual extension version bump
  and package rebuild still apply; the check that the committed package matches the extension folder
  catches a forgotten rebuild.

## Clarifications

### Session 2026-10-25

- Q: How should the extension README's per-agent sections relate to the single source? → A: Generate
  them from the source, moving material that only they carry into the agent's source file as further
  sections (FR-015).
- Q: Should each command file's own front-matter description come from the source? → A: Yes, generated
  from the same manifest description used for the extension manifest (FR-017).
- Q: Should other site pages that mention agents in passing (the scenario page, e-learning modules, the
  case study) be covered by the single source? → A: Not generated, but the check fails if any of them
  names an agent command the source does not ship (FR-024).
- Q: Can a section in an agent's source file be restricted to some outputs? → A: No; every section
  appears in both long-form outputs, so `AGENTS_LIST.md` and the extension README's per-agent sections
  carry identical text (FR-010, FR-015).
- Q: Who merges the existing copies into each agent's source file when seeding? → A: The
  implementation merges them — the full reference as the base, the extension README's extra sections
  added — and writes a seeding report of everything dropped or reworded for the maintainer to review
  (FR-016).
- Q: Where should a card's "Full reference" take the reader? → A: Nowhere; it is a collapsed section on
  the card that expands in place to show the agent's full description, so readers stay on the site and
  no anchor into `AGENTS_LIST.md` is needed (FR-011, SC-006).
- Refinements from planning: guides from the extension README sit after Examples (FR-004); the subset
  adds numbered lists and tables (FR-013); mechanism-only generator tests are replaced (SC-004).
- Refinements from analysis: phases carry no order field, their file order is the order (FR-005); the
  command-file description is owned by FR-017 alone (FR-012); the command-name guard also covers the
  hand-written parts of both READMEs (FR-024); SC-002 names the release steps a new agent still needs.

## Requirements *(mandatory)*

### Functional Requirements

**The source**

- **FR-001**: Agent information MUST live in one source directory, with exactly one file per agent,
  named by the agent's id.
- **FR-002**: Each agent file MUST begin with a flat header of `key: value` lines holding: id, title,
  command (when the agent has one), provider, type, phase, order (its position within the phase),
  status, summary, and manifest description (Spectra-shipped agents only). Unknown keys MUST be rejected.
- **FR-003**: The header MUST be readable with the Python standard library alone, on every Python version
  the repository supports, with no third-party parser.
- **FR-004**: A shipped Spectra agent's file MUST carry a body in this order: a lead paragraph, any
  further paragraphs, then the sections Arguments, Use it when, and Examples. Short labelled sections
  MAY appear between Use it when and Examples. Longer guides, such as walkthroughs and
  template-override steps, MAY appear after Examples. Planned agents and Spec Kit core agents MUST be
  header-only.
- **FR-005**: Phases (id, title, AI-DLC stage), in order, MUST live in a single phases file in the same
  directory, in the same header format.
- **FR-006**: The order of agents in every output MUST be deterministic and MUST reproduce today's
  roster order when seeded from today's content.

**What is generated**

- **FR-007**: The generator MUST write the roster data file (`agents-list.json`) from the source, with
  the same schema, field names, schema version, and order as today, so that installed copies of the
  `spectra` command and the Agent Roster page keep working without change.
- **FR-008**: The roster data file MUST become a generated output: hand edits to it MUST be reported by
  the check, and contributor documentation MUST stop telling people to edit it.
- **FR-009**: The generator MUST write every structured listing it writes today (the README agents
  table, the core-agent and roadmap sections of the full reference, the extension README command
  table) from the source rather than from the roster data file.
- **FR-010**: The generator MUST write every shipped agent's section of the full reference
  (`AGENTS_LIST.md`): heading, status, command, lead paragraph, further paragraphs, and every body
  section, in roster order.
- **FR-011**: The generator MUST write the Agent reference page's sidebar and cards: per shipped agent,
  its number, title, phase, command, lead paragraph, Arguments, Examples, and a collapsed Full
  reference section that expands in place, without scripts, to show the same text as the agent's
  section of the full reference. Everything outside the generated region (the page's own
  introduction, navigation, footer) stays hand-written.
- **FR-012**: The generator MUST write each Spectra command's description in the extension manifest
  from the agent's manifest description.
- **FR-013**: Formatting in the source MUST be limited to a defined Markdown subset — bold, italics,
  inline code, links, bulleted, numbered and nested lists, tables, and fenced code blocks — and
  converted to HTML for the Agent reference page with all text escaped. Anything outside the subset MUST stop generation with
  the file and line.
- **FR-014**: The Agent reference page MUST remain static HTML with no run-time fetch; the Agent Roster
  page keeps its existing run-time fetch of the roster data file.
- **FR-015**: The extension README's per-agent sections (`spectra/README.md`) MUST be generated from
  the same source. Material that today exists only there — numbered walkthroughs, template-override
  steps, upgrade notes — MUST move into the agent's source file as further titled sections, so it
  appears in the extension README and in the full reference alike.
  Every section of an agent's source file appears in both long-form outputs; there is no per-output
  marker, so the two carry identical text for each agent.
- **FR-016**: Seeding MUST be done by the implementation, not left to the maintainer: for each shipped
  agent the full reference (`AGENTS_LIST.md`) text is the base, sections that exist only in the
  extension README are added as further titled sections, and the manifest description becomes the
  `manifest` field. The implementation MUST write a seeding report in the feature directory listing,
  per agent and per copy, every sentence that did not carry over verbatim (dropped, reworded, or merged),
  so the maintainer reviews one report and one diff. Nothing is discarded without appearing in that
  report.
- **FR-017**: Each Spectra command file's front-matter description MUST be generated from the agent's
  manifest description, so the command file and the extension manifest carry the same text. Only the
  description line is generated; the rest of the command file stays hand-written.

**Checking**

- **FR-018**: The check mode MUST fail when any generated output differs from what the source would
  produce, naming each out-of-date output.
- **FR-019**: The check mode MUST fail when the set of shipped Spectra agents in the source differs from
  the commands registered in the extension manifest, naming each mismatch.
- **FR-020**: The check MUST run in CI and in the pre-ship checks exactly as the current generator check
  does, under the same CI job names, so the protected main branch stays pushable.
- **FR-021**: Every validation failure MUST name the file, and where applicable the line or field, that
  caused it.
- **FR-024**: Site pages that mention agents inside narrative (the scenarios page, the e-learning
  modules, the case study, and any other page under `docs/`), and the hand-written text outside the
  generated regions of `README.md` and `spectra/README.md`, are not generated and stay hand-written. The check MUST fail when any of them names a Spectra command
  (`speckit.spectra.<name>` or `/speckit-spectra-<name>`) that the source does not ship, naming the page
  and the command.

**Governance and documentation**

- **FR-022**: The constitution MUST be amended so Principle V names the agent source directory as the
  only source of truth for agent information, lists every generated output, and states that prose is
  authored by hand in the source and only rendered elsewhere.
- **FR-023**: Contributor and shipping documentation MUST describe adding or changing an agent as
  editing its source file and running the generator, and MUST stop naming the generated files as places
  to edit.

### Key Entities

- **Agent source file**: one agent; a header of facts (id, title, command, provider, type, phase,
  status, summary, manifest description) and, for shipped Spectra agents, a long description with
  named sections.
- **Phases file**: the ordered list of lifecycle phases, each with an id, title, and AI-DLC stage.
- **Roster data file** (`agents-list.json`): the published, machine-readable roster; now a generated
  output with an unchanged schema.
- **Generated region**: a delimited part of a hand-written file that the generator owns in full.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Changing any one fact about an existing agent requires editing exactly one file; zero
  outputs need a hand edit.
- **SC-002**: Adding a shipped agent requires creating exactly one source file for its information
  (plus the command itself, its manifest registration, and the Principle V release steps — version
  bump, changelog, catalog, package); the agent then appears in 100% of the outputs listed in FR-007
  through FR-012.
- **SC-003**: The roster data file generated from the seeded source is equivalent to today's file:
  every one of the 55 agents, every field, every value, in the same order.
- **SC-004**: 100% of the existing tests that read the roster, the full reference, the extension
  README, or the Agent reference page pass unchanged in what they assert. Tests of the mechanisms this
  feature removes on purpose — hand-written prose anchors, title matching, and the rule that
  descriptions are not compared — are replaced, not kept.
- **SC-005**: A stale output, a hand edit to a generated output, a missing required section, and a
  manifest mismatch are each caught by the check before a change can reach the main branch.
- **SC-006**: Every one of the 14 shipped agents' Agent reference cards carries a collapsed Full
  reference section whose text matches that agent's section of the full reference and opens with
  scripts disabled.

## Assumptions

- **Seeding text**: the full reference (`AGENTS_LIST.md`) is the most complete copy and becomes the
  source text; the Agent reference cards will therefore read a little differently from today's
  hand-written cards, which is accepted.
- **No new runtime dependency**: the generator stays maintainer tooling under `tools/`, standard
  library only; nothing new ships to users' machines.
- **Shipped vs generated**: the roster data file, the full reference, the README files, the extension
  manifest, and the Agent reference page stay committed to the repository so it reads correctly for
  someone who never runs the generator.
- **Extension versioning**: a change that alters a shipped file (the extension README, the manifest, or
  a command file's description)
  follows the existing rules — extension version bump, changelog entry, package rebuild — in the same
  change. This feature itself changes shipped text (the extension README's per-agent sections are
  regenerated, and command-file descriptions are unified with the manifest's), so it carries a bump.
- **Spec Kit core agents** stay listed in the roster and the full reference by their one-line summary
  only; they get no long description and no Agent reference card.
- **Order** is expressed in the source explicitly, by each agent's `order` field within its phase,
  rather than derived from file names.
- **Out of scope**: rewriting the narrative pages that teach with agents (scenarios, e-learning, case
  study). They stay hand-written; FR-024 only guards their command names.
- **The constitution amendment** is made with `/speckit-constitution` after clarification and before
  planning, so the plan's Constitution Check is evaluated against the amended Principle V.
- **The CLI's roster parser** (`spectra_cli/roster.py`) is unchanged; the generator may keep using it
  to validate the roster data file it produces.
