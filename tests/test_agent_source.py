"""`agents/`, the only source of truth for agent information (feature 040, data-model.md).

Every validation rule is exercised against a throwaway directory, and every failure is asserted to
name the file — and the line or field where one applies — because a maintainer who has to hunt for
the problem will fix it in the wrong place.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import agent_source  # noqa: E402

PHASES = """---
id: foundation
title: Foundation
aidlc: Inception
---

---
id: testing-quality
title: Testing & Quality
aidlc: Construction
---
"""

BODY = """
Lead paragraph with **bold**.

A further paragraph.

## Arguments

none needed.

## Use it when

you want to.

## Where it writes

`docs/` by default.

## Examples

```
/speckit-spectra-demo
/speckit-spectra-demo --flag
```

## A guide

1. step one
2. step two
"""


def header(**fields):
    base = {"id": "demo", "title": "Demo", "command": "speckit.spectra.demo", "provider": "spectra",
            "type": "add-on", "phase": "foundation", "order": "10", "status": "available",
            "summary": "Does a thing: with a colon, \"quotes\" — and a dash.",
            "manifest": "Do the thing."}
    base.update(fields)
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in base.items() if v is not None) + "---\n"


class Sandbox:
    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "agents"
        self.root.mkdir()
        (self.root / "_phases.md").write_text(PHASES, encoding="utf-8")

    def write(self, name, text):
        (self.root / name).write_text(text, encoding="utf-8")

    def load(self):
        return agent_source.load(self.root)

    def problems(self):
        with self.assertRaises_source() as caught:
            self.load()
        return caught

    def assertRaises_source(self):  # noqa: N802 - mirrors unittest naming
        return _Catcher()

    def close(self):
        self._tmp.cleanup()


class _Catcher:
    def __enter__(self):
        self.problems = None
        return self

    def __exit__(self, kind, exc, tb):
        if kind is None:
            raise AssertionError("expected SourceError, but the source loaded")
        if not issubclass(kind, agent_source.SourceError):
            return False
        self.problems = exc.problems
        return True


class Base(unittest.TestCase):
    def setUp(self):
        self.box = Sandbox()
        self.addCleanup(self.box.close)

    def problems_for(self, name, text):
        self.box.write(name, text)
        catcher = self.box.problems()
        return catcher.problems

    def assertProblem(self, problems, *fragments):  # noqa: N802
        joined = "\n".join(problems)
        for fragment in fragments:
            self.assertIn(fragment, joined)


class ValidSource(Base):

    def test_a_shipped_agent_loads_with_its_body_split(self):
        self.box.write("demo.md", header() + BODY)
        source = self.box.load()
        agent = source.agents[0]
        self.assertTrue(agent.shipped)
        self.assertEqual(agent.number, 1)
        self.assertEqual(agent.body.lead, ["Lead paragraph with **bold**."])
        self.assertEqual(agent.body.further, ["A further paragraph."])
        self.assertEqual([s.label for s in agent.body.items],
                         ["Arguments", "Use it when", "Where it writes", "Examples"])
        self.assertEqual([s.label for s in agent.body.guides], ["A guide"])
        self.assertEqual(agent.body.examples, ["/speckit-spectra-demo", "/speckit-spectra-demo --flag"])

    def test_header_values_are_literal(self):
        self.box.write("demo.md", header() + BODY)
        self.assertEqual(self.box.load().agents[0].summary,
                         "Does a thing: with a colon, \"quotes\" — and a dash.")

    def test_order_is_phase_then_order(self):
        self.box.write("b.md", header(id="b", command="speckit.plan", provider="speckit", type="core",
                                      phase="testing-quality", order="10", manifest=None))
        self.box.write("c.md", header(id="c", command="speckit.plan", provider="speckit", type="core",
                                      order="20", manifest=None))
        self.box.write("a.md", header(id="a", command="speckit.plan", provider="speckit", type="core",
                                      order="30", manifest=None))
        self.assertEqual([a.id for a in self.box.load().agents], ["c", "a", "b"])

    def test_two_agents_may_share_a_command(self):
        for agent_id, order in (("implement", "10"), ("testing", "20")):
            self.box.write(f"{agent_id}.md", header(id=agent_id, command="speckit.implement",
                                                    provider="speckit", type="core", order=order,
                                                    manifest=None))
        self.assertEqual(len(self.box.load().agents), 2)

    def test_the_label_joiner(self):
        section = agent_source.Section("Re-runs ask first.", [], 1)
        self.assertEqual(section.joiner, " ")
        self.assertEqual(agent_source.Section("Template", [], 1).joiner, " — ")


class HeaderRules(Base):

    def test_unknown_field(self):
        self.assertProblem(self.problems_for("demo.md", header(colour="blue") + BODY),
                           "agents/demo.md:", "unknown field `colour`")

    def test_missing_field(self):
        self.assertProblem(self.problems_for("demo.md", header(summary=None) + BODY),
                           "agents/demo.md:1", "missing required field `summary`")

    def test_duplicate_field(self):
        text = header().replace("title: Demo\n", "title: Demo\ntitle: Again\n") + BODY
        self.assertProblem(self.problems_for("demo.md", text), "agents/demo.md:4",
                           "`title` appears twice")

    def test_line_without_key_value(self):
        text = header().replace("title: Demo\n", "title Demo\n") + BODY
        self.assertProblem(self.problems_for("demo.md", text), "agents/demo.md:3",
                           "`key: value`")

    def test_unterminated_header(self):
        self.assertProblem(self.problems_for("demo.md", header()[:-4]), "never closed")

    def test_enum_values(self):
        self.assertProblem(self.problems_for("demo.md", header(status="maybe") + BODY),
                           "agents/demo.md:", "`status` must be one of available, planned")

    def test_unknown_phase(self):
        self.assertProblem(self.problems_for("demo.md", header(phase="nowhere") + BODY),
                           "unknown phase 'nowhere'")

    def test_order_must_be_a_positive_integer(self):
        self.assertProblem(self.problems_for("demo.md", header(order="first") + BODY),
                           "`order` must be a positive integer")

    def test_id_must_match_file_name(self):
        self.assertProblem(self.problems_for("demo.md", header(id="other") + BODY),
                           "does not match the file name")

    def test_duplicate_position(self):
        self.box.write("other.md", header(id="other", command="speckit.plan", provider="speckit",
                                          type="core", manifest=None))
        self.assertProblem(self.problems_for("demo.md", header() + BODY),
                           "order 10 in phase 'foundation' is already taken")

    def test_manifest_only_on_shipped_agents(self):
        self.assertProblem(
            self.problems_for("demo.md", header(status="planned", command=None)),
            "only a shipped Spectra agent has a `manifest`")

    def test_planned_agent_records_no_command(self):
        text = header(status="planned", manifest=None)
        self.assertProblem(self.problems_for("demo.md", text),
                           "agents/demo.md:4: a planned agent records no command")

    def test_available_agent_needs_a_command(self):
        text = header(command=None, provider="speckit", type="core", manifest=None)
        self.assertProblem(self.problems_for("demo.md", text),
                           "agents/demo.md:1", "an available agent needs a `command`")

    def test_shipped_agent_needs_manifest(self):
        self.assertProblem(self.problems_for("demo.md", header(manifest=None) + BODY),
                           "needs a `manifest` description")

    def test_shipped_command_is_named_after_the_id(self):
        self.assertProblem(self.problems_for("demo.md", header(command="speckit.spectra.x") + BODY),
                           "must be 'speckit.spectra.demo'")

    def test_stray_file(self):
        self.assertProblem(self.problems_for("Notes.txt", "hello"), "agents/Notes.txt",
                           "not an agent file")


class BodyRules(Base):

    def test_body_on_planned_agent(self):
        text = header(status="planned", manifest=None) + "\nA body that should not be here.\n"
        self.assertProblem(self.problems_for("demo.md", text), "agents/demo.md:13",
                           "only a shipped Spectra agent has a body")

    def test_shipped_agent_without_body(self):
        self.assertProblem(self.problems_for("demo.md", header()), "needs a long description")

    def test_missing_examples(self):
        body = BODY.split("## Examples")[0]
        self.assertProblem(self.problems_for("demo.md", header() + body),
                           "agents/demo.md", "missing required section \"Examples\"")

    def test_arguments_must_come_first(self):
        body = BODY.replace("## Arguments\n\nnone needed.\n\n## Use it when\n\nyou want to.\n",
                            "## Use it when\n\nyou want to.\n\n## Arguments\n\nnone needed.\n")
        self.assertProblem(self.problems_for("demo.md", header() + body),
                           "\"Arguments\" must be section 1")

    def test_arguments_shape(self):
        body = BODY.replace("none needed.", "one.\n\ntwo.")
        self.assertProblem(self.problems_for("demo.md", header() + body),
                           "\"Arguments\" must be one paragraph")

    def test_examples_must_be_one_fence(self):
        body = BODY.replace("```\n/speckit-spectra-demo\n", "run it\n\n```\n/speckit-spectra-demo\n")
        self.assertProblem(self.problems_for("demo.md", header() + body),
                           "\"Examples\" must be exactly one fenced code block")

    def test_deeper_heading(self):
        body = BODY.replace("## A guide", "### A guide")
        self.assertProblem(self.problems_for("demo.md", header() + body),
                           "only `## ` headings")

    def test_unsupported_markdown_names_its_line(self):
        body = BODY.replace("A further paragraph.", "A <b>raw</b> paragraph.")
        problems = self.problems_for("demo.md", header() + body)
        self.assertProblem(problems, "agents/demo.md:16:", "raw HTML")

    def test_every_problem_is_reported_at_once(self):
        self.box.write("one.md", header(id="one", status="maybe") + BODY)
        problems = self.problems_for("two.md", header(id="two", colour="x") + BODY)
        self.assertProblem(problems, "agents/one.md", "agents/two.md")


if __name__ == "__main__":
    unittest.main()
