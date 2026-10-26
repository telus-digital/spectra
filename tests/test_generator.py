"""The agent documentation generator, rendering every output from `agents/` (feature 040).

Every test runs against a *copy* of the real committed source and outputs, with the generator's
repository root pointed at the copy. That way the tests assert on the structure actually shipped —
markers, anchors, cards, description lines — while never risking the working tree.
"""

from __future__ import annotations

import contextlib
import html
import importlib.util
import io
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

OUTPUTS = ("agents-list.json", "README.md", "AGENTS_LIST.md", "spectra/README.md",
           "spectra/extension.yml", "docs/getting-started/agents.html")
LONG_FORM = ("AGENTS_LIST.md", "spectra/README.md", "docs/getting-started/agents.html")


def _load_generator():
    """Import `tools/generate_agent_docs.py` by path — it is a script, not a package."""
    path = h.repo_file("tools", "generate_agent_docs.py")
    spec = importlib.util.spec_from_file_location("generate_agent_docs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gen = _load_generator()


@contextlib.contextmanager
def sandbox():
    """A throwaway copy of the source and every output, with the generator pointed at it."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relative in ("agents", "spectra/commands"):
            shutil.copytree(h.repo_file(*relative.split("/")), root / relative)
        shutil.copytree(h.repo_file("docs"), root / "docs",
                        ignore=lambda directory, names: ["packages"] if directory.endswith("docs")
                        else [])
        for relative in OUTPUTS:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(h.repo_file(*relative.split("/")), destination)
        with mock.patch.object(gen, "REPO_ROOT", root):
            yield root


def run(root, argv=None):
    """Run the generator, returning (exit code, stdout + stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = gen.main(argv or [])
    return code, out.getvalue() + err.getvalue()


def every_file(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*")) if path.is_file()}


def changed(before, root):
    after = every_file(root)
    return {name for name in after if before.get(name) != after[name]}


def edit(root, relative, old, new):
    path = root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text, (relative, old)
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def outside_generated(text):
    """Everything a human owns: the file with every region and generator-owned line removed."""
    text = re.sub(r"<!-- SPECTRA:GENERATED START.*?<!-- SPECTRA:GENERATED END id=[a-z0-9-]+ -->",
                  "", text, flags=re.S)
    return re.sub(r'^ *description: ".*"$', "", text, flags=re.M)


def agents_list_block(text, agent_id):
    start = text.index(f"<!-- SPECTRA:AGENT id={agent_id} -->")
    nxt = text.find("<!-- SPECTRA:AGENT id=", start + 1)
    end = nxt if nxt != -1 else text.index("<!-- SPECTRA:GENERATED END id=agents-list-shipped")
    return text[start:end]


def readme_section(text, command):
    start = text.index(f"## `{command}`")
    nxt = text.find("\n## `speckit.spectra.", start + 1)
    end = nxt if nxt != -1 else text.index("<!-- SPECTRA:GENERATED END id=spectra-readme-agents")
    return text[start:end]


def card(text, agent_id):
    start = text.index(f'<li class="agent" id="a-{agent_id}">')
    return text[start:text.index("\n        </li>", start)]


def words(text):
    return re.findall(r"[A-Za-z0-9]+", text)


def markdown_words(block, agent_id):
    """A long-form Markdown section reduced to its words, minus its title and command prefix.

    Fence info strings and ordered-list numbers are markup on the HTML side, so they go too.
    """
    lines = [line for line in block.split("\n") if not line.startswith("<!--")][1:]
    text = "\n".join(re.sub(r"^(\s*)\d+\. ", r"\1", re.sub(r"^(\s*)```\S+$", r"\1```", line))
                     for line in lines)
    found = words(re.sub(r"\]\([^)]+\)", "]", text))
    prefix = words(f"speckit.spectra.{agent_id}")
    return found[len(prefix):] if found[:len(prefix)] == prefix else found


def html_words(fragment):
    fragment = re.sub(r'(?:href|class|start)="[^"]*"', "", fragment)
    return words(html.unescape(re.sub(r"<[^>]+>", " ", fragment)))


class CommittedStateIsCurrent(unittest.TestCase):
    def test_the_repository_as_committed_passes_check(self):
        """If this fails, someone edited agents/ without regenerating, or edited an output by hand."""
        code, out = run(None, ["--check"])
        self.assertEqual(code, 0, out)


class Determinism(unittest.TestCase):
    def test_two_consecutive_runs_produce_identical_files(self):
        with sandbox() as root:
            run(root)
            first = every_file(root)
            run(root)
            self.assertEqual(every_file(root), first)

    def test_running_on_already_current_outputs_changes_nothing(self):
        with sandbox() as root:
            run(root)
            before = every_file(root)
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertIn("already current", out)
            self.assertEqual(before, every_file(root))


class HandWrittenTextIsUntouched(unittest.TestCase):
    def test_everything_outside_regions_and_named_lines_is_byte_identical(self):
        """The guarantee that makes generated and hand-written content safe to interleave."""
        with sandbox() as root:
            edit(root, "agents/adr.md", "Create a context-aware", "Write a context-aware")
            edit(root, "agents/adr.md", "manifest: Create a new", "manifest: Draft a new")
            names = [n for n in OUTPUTS if n != "agents-list.json"] + ["spectra/commands/adr.md"]
            before = {n: outside_generated((root / n).read_text(encoding="utf-8")) for n in names}
            code, out = run(root)
            self.assertEqual(code, 0, out)
            after = {n: outside_generated((root / n).read_text(encoding="utf-8")) for n in names}
        self.assertEqual(before, after)

    def test_a_marker_line_is_never_duplicated_by_a_run(self):
        with sandbox() as root:
            run(root)
            run(root)
            for relative in LONG_FORM:
                text = (root / relative).read_text(encoding="utf-8")
                for region in re.findall(r"SPECTRA:GENERATED START id=([a-z0-9-]+)", text):
                    self.assertEqual(text.count(f"SPECTRA:GENERATED START id={region} "), 1)


class RosterFileIsUnchanged(unittest.TestCase):
    """User Story 3 — installed CLIs and docs/agents.html read this file at run time."""

    def test_the_generated_roster_is_byte_identical_to_the_committed_one(self):
        with sandbox() as root:
            source = gen.agent_source.load(root / "agents")
            self.assertEqual(gen.render_roster_json(source),
                             h.repo_file("agents-list.json").read_text(encoding="utf-8"))

    def test_a_hand_edit_to_the_roster_fails_check_and_names_it(self):
        with sandbox() as root:
            edit(root, "agents-list.json", '"title": "Guardrails"', '"title": "Edited"')
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        self.assertIn("agents-list.json: does not match what agents/ renders", out)

    def test_the_built_roster_passes_the_cli_parser(self):
        from spectra_cli import roster as roster_module
        with sandbox() as root:
            run(root)
            roster = roster_module.load(root / "agents-list.json", strict=True)
        self.assertEqual(len(roster.shipped()), 14)


class OneEditEverywhere(unittest.TestCase):
    """User Story 1 — change an agent's description in one place."""

    def test_a_lead_change_reaches_every_long_form_output_and_nothing_else(self):
        with sandbox() as root:
            before = every_file(root)
            edit(root, "agents/adr.md", "Create a context-aware", "Write a context-aware")
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertEqual(changed(before, root), {"agents/adr.md", *LONG_FORM})
            for relative in LONG_FORM:
                self.assertIn("Write a context-aware", (root / relative).read_text(encoding="utf-8"))

    def test_a_summary_change_reaches_the_roster_and_the_commands_table(self):
        with sandbox() as root:
            before = every_file(root)
            edit(root, "agents/adr.md", "summary: Capture a", "summary: Record a")
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertEqual(changed(before, root),
                             {"agents/adr.md", "agents-list.json", "spectra/README.md"})

    def test_a_manifest_change_reaches_both_description_lines_identically(self):
        with sandbox() as root:
            before = every_file(root)
            edit(root, "agents/adr.md", "manifest: Create a new", 'manifest: Draft a "new"')
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertEqual(changed(before, root), {"agents/adr.md", "spectra/extension.yml",
                                                     "spectra/commands/adr.md"})
            expected = 'description: "Draft a \\"new\\" Architecture Decision Record'
            self.assertIn(expected, (root / "spectra/extension.yml").read_text(encoding="utf-8"))
            self.assertIn(expected, (root / "spectra/commands/adr.md").read_text(encoding="utf-8"))

    def test_a_source_change_without_regeneration_fails_check(self):
        with sandbox() as root:
            edit(root, "agents/adr.md", "Create a context-aware", "Write a context-aware")
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        for relative in LONG_FORM:
            self.assertIn(f"{relative}: does not match", out)

    def test_a_hand_edit_in_any_generated_output_fails_check_and_names_it(self):
        edits = (
            ("README.md", "| Guardrails |", "| Guardrails EDITED |"),
            ("AGENTS_LIST.md", "### Domain Analyzer ✅", "### Domain Analyser ✅"),
            ("spectra/README.md", "## `speckit.spectra.uat` — UAT Runner", "## `speckit.spectra.uat` — UAT"),
            ("docs/getting-started/agents.html", "<h3>Create PR</h3>", "<h3>Open PR</h3>"),
            ("spectra/extension.yml", "and hand any constitution change", "and hand constitution changes"),
            ("spectra/commands/adr.md", "and hand any constitution change", "and hand constitution changes"),
        )
        for relative, old, new in edits:
            with self.subTest(file=relative), sandbox() as root:
                edit(root, relative, old, new)
                code, out = run(root, ["--check"])
                self.assertEqual(code, 1)
                self.assertIn(f"{relative}: does not match what agents/ renders", out)

    def test_check_never_writes(self):
        with sandbox() as root:
            edit(root, "agents/adr.md", "Create a context-aware", "Write a context-aware")
            before = every_file(root)
            run(root, ["--check"])
            self.assertEqual(before, every_file(root))

    def test_both_long_form_outputs_carry_identical_text(self):
        """FR-015 — no per-output section markers: the README and the full reference agree."""
        agents_list = h.repo_file("AGENTS_LIST.md").read_text(encoding="utf-8")
        readme = h.repo_file("spectra", "README.md").read_text(encoding="utf-8")
        for agent_id in ("adr", "kb-vault", "review-pr", "test-plan"):
            with self.subTest(agent=agent_id):
                self.assertEqual(
                    markdown_words(agents_list_block(agents_list, agent_id), agent_id),
                    markdown_words(readme_section(readme, f"speckit.spectra.{agent_id}"), agent_id))


class InvalidInputWritesNothing(unittest.TestCase):

    def test_an_invalid_source_is_reported_before_anything_is_written(self):
        with sandbox() as root:
            edit(root, "agents/adr.md", "## Examples", "## Samples")
            before = every_file(root)
            code, out = run(root)
            self.assertEqual(code, 1)
            self.assertIn("agents/adr.md", out)
            self.assertIn('missing required section "Examples"', out)
            self.assertEqual(before, every_file(root))

    def test_unsupported_markdown_is_refused_with_file_and_line(self):
        with sandbox() as root:
            edit(root, "agents/adr.md", "Create a context-aware", "Create a <b>raw</b>")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertRegex(out, r"agents/adr\.md:\d+: raw HTML")

    def test_a_missing_end_marker_fails_and_leaves_the_file_unwritten(self):
        with sandbox() as root:
            path = root / "README.md"
            edit(root, "README.md", "<!-- SPECTRA:GENERATED END id=readme-agents-table -->", "")
            broken = path.read_text(encoding="utf-8")
            code, out = run(root)
            self.assertEqual(code, 1)
            self.assertIn("README.md: missing end marker", out)
            self.assertEqual(path.read_text(encoding="utf-8"), broken)

    def test_a_missing_start_marker_fails(self):
        with sandbox() as root:
            edit(root, "AGENTS_LIST.md", "<!-- SPECTRA:GENERATED START id=agents-list-shipped -->", "")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertIn("missing start marker for region 'agents-list-shipped'", out)

    def test_a_duplicated_region_fails(self):
        with sandbox() as root:
            path = root / "README.md"
            path.write_text(path.read_text(encoding="utf-8")
                            + "\n<!-- SPECTRA:GENERATED START id=readme-agents-table -->\n"
                              "<!-- SPECTRA:GENERATED END id=readme-agents-table -->\n",
                            encoding="utf-8")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertIn("appears 2 times", out)

    def test_an_unknown_region_id_fails_rather_than_being_ignored(self):
        with sandbox() as root:
            path = root / "README.md"
            path.write_text(path.read_text(encoding="utf-8")
                            + "\n<!-- SPECTRA:GENERATED START id=invented-region -->\n"
                              "<!-- SPECTRA:GENERATED END id=invented-region -->\n",
                            encoding="utf-8")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertIn("invented-region", out)

    def test_a_missing_description_line_fails_and_names_the_file(self):
        with sandbox() as root:
            edit(root, "spectra/commands/uat.md", "description:", "summary:")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertIn("spectra/commands/uat.md: expected exactly one generated description line", out)


class AddingAnAgent(unittest.TestCase):
    """User Story 2 — one new file, and mismatches with the manifest are named."""

    PLANNED = ("---\nid: demo\ntitle: Demo Agent\nprovider: spectra\ntype: add-on\n"
               "phase: testing-quality\norder: 45\nstatus: planned\nsummary: A demonstration.\n---\n")

    def test_a_planned_agent_appears_in_the_roster_table_and_roadmap_only(self):
        with sandbox() as root:
            before = every_file(root)
            (root / "agents" / "demo.md").write_text(self.PLANNED, encoding="utf-8")
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertEqual(changed(before, root),
                             {"agents/demo.md", "agents-list.json", "README.md", "AGENTS_LIST.md"})
            roadmap = (root / "AGENTS_LIST.md").read_text(encoding="utf-8").split(
                "SPECTRA:GENERATED START id=agents-list-roadmap")[1]
            self.assertIn("**Demo Agent** (Add-on) — A demonstration.", roadmap)

    def test_order_places_the_agent_between_its_neighbours(self):
        with sandbox() as root:
            (root / "agents" / "demo.md").write_text(self.PLANNED, encoding="utf-8")
            run(root)
            source = gen.agent_source.load(root / "agents")
            ids = [a.id for a in source.agents if a.phase == "testing-quality"]
            orders = {a.id: a.order for a in source.agents}
        position = ids.index("demo")
        self.assertLess(orders[ids[position - 1]], 45)
        self.assertGreater(orders[ids[position + 1]], 45)

    def test_a_shipped_agent_the_manifest_does_not_register_fails(self):
        with sandbox() as root:
            text = (root / "agents" / "uat.md").read_text(encoding="utf-8")
            text = (text.replace("id: uat", "id: demo").replace("speckit.spectra.uat",
                                                                "speckit.spectra.demo")
                    .replace("order: ", "order: 9"))
            (root / "agents" / "demo.md").write_text(text, encoding="utf-8")
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        self.assertIn("agents/demo.md declares 'speckit.spectra.demo', which spectra/extension.yml "
                      "does not register", out)
        self.assertIn("spectra/commands/demo.md does not exist", out)

    def test_a_registered_command_with_no_source_fails(self):
        with sandbox() as root:
            text = (root / "agents" / "uat.md").read_text(encoding="utf-8")
            header = text.split("\n---\n")[0].replace("status: available", "status: planned")
            header = "\n".join(line for line in header.split("\n")
                               if not line.startswith(("command:", "manifest:")))
            (root / "agents" / "uat.md").write_text(header + "\n---\n", encoding="utf-8")
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        self.assertIn("spectra/extension.yml registers 'speckit.spectra.uat'", out)

    def test_a_planned_agent_with_a_command_names_its_file_and_line(self):
        with sandbox() as root:
            edit(root, "agents/gdpr.md", "status: planned", "status: planned\ncommand: speckit.gdpr")
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertRegex(out, r"agents/gdpr\.md:\d+: a planned agent records no command")

    def test_a_title_change_keeping_the_id_propagates_and_still_verifies(self):
        with sandbox() as root:
            edit(root, "agents/gdpr.md", "title: GDPR Compliance", "title: GDPR Readiness")
            code, out = run(root)
            self.assertEqual(code, 0, out)
            for relative in ("README.md", "AGENTS_LIST.md", "agents-list.json"):
                text = (root / relative).read_text(encoding="utf-8")
                self.assertIn("GDPR Readiness", text)
                self.assertNotIn("GDPR Compliance", text)
            code, out = run(root, ["--check"])
        self.assertEqual(code, 0, out)


class AgentReferencePage(unittest.TestCase):
    """User Story 4 — the sidebar and cards are generated static HTML (agents-page-markup.md)."""

    @classmethod
    def setUpClass(cls):
        cls.page = h.repo_file("docs", "getting-started", "agents.html").read_text(encoding="utf-8")
        cls.agents_list = h.repo_file("AGENTS_LIST.md").read_text(encoding="utf-8")
        cls.source = gen.agent_source.load(h.repo_file("agents"))

    def test_sidebar_and_cards_follow_the_roster_numbered_from_01(self):
        shipped = [a.id for a in self.source.shipped()]
        self.assertEqual(re.findall(r'<a href="#a-([a-z-]+)"><span class="n">', self.page), shipped)
        self.assertEqual(re.findall(r'<li class="agent" id="a-([a-z-]+)">', self.page), shipped)
        self.assertEqual(re.findall(r'<header><span class="n">(\d\d)</span>', self.page),
                         [f"{n:02d}" for n in range(1, len(shipped) + 1)])

    def test_card_invariants(self):
        for agent in self.source.shipped():
            with self.subTest(agent=agent.id):
                text = card(self.page, agent.id)
                cdesc = text[text.index('class="cdesc"'):]
                cdesc = cdesc[:cdesc.index("</span>")]
                self.assertNotIn("<span", cdesc[len('class="cdesc">'):])
                args = text[text.index('class="args"'):text.index("</div>", text.index('class="args"'))]
                self.assertNotIn("<span", args)
                first = re.search(r"<pre><code>(.*?)</code></pre>", text).group(1)
                self.assertEqual(html.unescape(first), agent.body.examples[0])
                self.assertGreater(text.index('<details class="fullref">'),
                                   text.rindex("<pre><code>", 0, text.index("<details")))

    def test_the_full_reference_carries_the_same_text_as_agents_list(self):
        """SC-006."""
        for agent in self.source.shipped():
            with self.subTest(agent=agent.id):
                text = card(self.page, agent.id)
                body = text[text.index('<div class="fullref-body">'):]
                self.assertEqual(html_words(body),
                                 markdown_words(agents_list_block(self.agents_list, agent.id),
                                                agent.id))

    def test_emphasis_in_the_lead_carries_over(self):
        """US4 acceptance scenario 3."""
        for agent in self.source.shipped():
            with self.subTest(agent=agent.id):
                lead = "\n".join(agent.body.lead)
                cdesc = card(self.page, agent.id).split('class="cdesc">')[1].split("</span>")[0]
                if re.search(r"\*\*(.+?)\*\*", lead, re.S):
                    self.assertIn("<b>", cdesc)
                for inner in re.findall(r"`([^`]+)`", lead):
                    self.assertIn(f"<code>{html.escape(inner, quote=False)}</code>", cdesc)

    def test_the_generated_regions_fetch_nothing(self):
        regions = re.findall(r"SPECTRA:GENERATED START id=agents-page-[a-z]+ -->(.*?)<!-- SPECTRA",
                             self.page, re.S)
        self.assertEqual(len(regions), 2)
        for region in regions:
            self.assertNotIn("fetch(", region)
            self.assertNotIn("<script", region)

    def test_an_unknown_command_on_a_narrative_page_fails_check(self):
        """FR-024."""
        with sandbox() as root:
            edit(root, "docs/e-learning/module-1.html", "speckit.spectra.adr", "speckit.spectra.adrx")
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        self.assertIn("docs/e-learning/module-1.html: names speckit.spectra.adrx", out)

    def test_hand_written_readme_text_is_guarded_too(self):
        with sandbox() as root:
            edit(root, "spectra/README.md", "/speckit.spectra.domain-analyzer", "/speckit.spectra.nope")
            code, out = run(root, ["--check"])
        self.assertEqual(code, 1)
        self.assertIn("spectra/README.md: names speckit.spectra.nope", out)


class Renderers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = gen.agent_source.load(h.repo_file("agents"))
        cls.roster = gen.build_roster(cls.source)

    def render(self, renderer):
        return "\n".join(renderer(self.roster, self.source))

    def test_the_readme_table_has_one_row_per_agent(self):
        rows = [line for line in gen.render_readme_table(self.roster, self.source)
                if line.startswith("| ")]
        self.assertEqual(len(rows) - 2, len(self.roster.agents))  # minus header and separator

    def test_the_readme_table_names_every_spec_kit_agent_in_its_sentence(self):
        rendered = self.render(gen.render_readme_table)
        for agent in self.roster.agents:
            if agent.provider == "speckit" and agent.available:
                self.assertIn(agent.title, rendered)

    def test_the_roadmap_lists_only_planned_agents(self):
        rendered = self.render(gen.render_roadmap)
        for agent in self.roster.agents:
            if agent.available:
                self.assertNotIn(f"**{agent.title}**", rendered)
            else:
                self.assertIn(f"**{agent.title}**", rendered)

    def test_the_speckit_section_lists_only_spec_kit_agents(self):
        rendered = self.render(gen.render_speckit_core)
        for agent in self.roster.agents:
            if agent.provider == "spectra":
                self.assertNotIn(f"### {agent.title} —", rendered)

    def test_the_shipped_sections_are_anchored_by_id_in_roster_order(self):
        rendered = self.render(gen.render_agents_list_shipped)
        self.assertEqual(re.findall(r"<!-- SPECTRA:AGENT id=([a-z-]+) -->", rendered),
                         [a.id for a in self.source.shipped()])

    def test_the_claude_trigger_uses_dashes(self):
        self.assertEqual(gen._claude_trigger("speckit.spectra.adr"), "/speckit-spectra-adr")

    def test_the_extension_readme_table_lists_only_shipped_agents(self):
        self.assertEqual(self.render(gen.render_spectra_commands).count("| `speckit."),
                         len(self.roster.shipped()))

    def test_every_region_writes_unix_line_endings(self):
        for region in gen.REGIONS:
            self.assertNotIn("\r", gen.render_region(region, self.roster, self.source))

    def test_the_description_line_escapes_quotes_and_backslashes(self):
        self.assertEqual(gen._description_line('a "b" \\ c'), 'description: "a \\"b\\" \\\\ c"')


class WritePath(unittest.TestCase):
    """The rendered string is not the guarantee — what lands on disk is.

    An earlier version of the writer asked the text layer for `\\n` via
    `Path.write_text(newline=...)`, which only exists on Python 3.10+ and crashed on the 3.9 floor
    `pyproject.toml` declares. Rendering was correct; writing was not. So these assert on bytes.
    """

    def test_a_run_writes_no_carriage_returns(self):
        with sandbox() as root:
            edit(root, "agents/adr.md", "Create a context-aware", "Write a context-aware")
            code, out = run(root)
            self.assertEqual(code, 0, out)
            for relative in OUTPUTS:
                self.assertNotIn(b"\r", (root / relative).read_bytes(), relative)

    def test_crlf_input_is_normalized_rather_than_preserved(self):
        with sandbox() as root:
            path = root / "README.md"
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertNotIn(b"\r", path.read_bytes(),
                             "a CRLF checkout must come out normalized, not rewritten as CRLF")

    def test_the_writer_does_not_depend_on_a_python_3_10_only_api(self):
        """Parsed, not grepped — the source explains this pitfall in prose, and prose is not a call."""
        import ast

        offenders = []
        for name in ("generate_agent_docs.py", "agent_source.py", "markdown_subset.py"):
            source = h.repo_file("tools", name).read_text(encoding="utf-8")
            for node in ast.walk(ast.parse(source)):
                if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "write_text" \
                        and "newline" in {kw.arg for kw in node.keywords if kw.arg}:
                    offenders.append(f"{name}:{node.lineno}: write_text(newline=...)")
        self.assertEqual(offenders, [],
                         "Path.write_text(newline=...) is 3.10+ and pyproject declares a 3.9 floor; "
                         "write bytes instead")


if __name__ == "__main__":
    unittest.main()
