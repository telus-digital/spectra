"""The brownfield onboarding sequence is told the same way everywhere a newcomer might read it (spec 036).

Three hand-written surfaces carry a "Starting on an existing codebase" section: the repository README,
the extension README, and the published landing page. Each lists the five foundation agents in order with
a constitution run after every feeder. A sequence that drifted on one surface would send a newcomer to run
the agents in an order where a later one re-proposes what an earlier one already ratified — so the order
is asserted here, against each surface and against the methodology agent's own next-agent line.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

SURFACES = {
    "README.md": h.repo_file("README.md"),
    "spectra/README.md": h.repo_file("spectra", "README.md"),
    "docs/index.html": h.repo_file("docs", "index.html"),
}
METHODOLOGY = h.repo_file("spectra", "commands", "methodology.md")

HEADING = "Starting on an existing codebase"
EXPECTED = [
    "kb-vault",
    "domain-analyzer",
    "constitution",
    "methodology",
    "constitution",
    "test-strategy",
    "constitution",
    "deployment-strategy",
    "constitution",
]
FEEDERS = ["domain-analyzer", "methodology", "test-strategy", "deployment-strategy"]
TOKEN = re.compile(r"speckit-(?:spectra-)?(kb-vault|domain-analyzer|methodology|test-strategy|deployment-strategy|constitution)")


def section(path: Path) -> str:
    """The text of the onboarding section, from its heading to the next heading of the same level."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        start = text.index(f"{HEADING}</h2>")
        end = text.index("</section>", start)
    else:
        start = text.index(f"## {HEADING}")
        end = text.find("\n## ", start + 1)
    return text[start : end if end != -1 else None]


def procedure(body: str) -> list:
    """The agents named by the numbered procedure, in order — list items only, never the prose around it."""
    if "<li>" in body:
        items = re.findall(r"<li>(.*?)</li>", body, re.S)
    else:
        items = re.findall(r"^\d+\. (.*(?:\n {3}.*)*)", body, re.M)
    return [m.group(1) for item in items for m in TOKEN.finditer(item)]


def flat(text: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", "", text).split())


class TheSequenceIsTheSameEverywhere(unittest.TestCase):
    def test_each_surface_lists_the_sequence_in_order(self):
        for name, path in SURFACES.items():
            with self.subTest(surface=name):
                self.assertEqual(procedure(section(path)), EXPECTED)

    def test_the_three_surfaces_agree(self):
        sequences = {name: tuple(procedure(section(path))) for name, path in SURFACES.items()}
        self.assertEqual(len(set(sequences.values())), 1, sequences)

    def test_the_feeder_order_matches_the_methodology_hand_on(self):
        line = next(
            line for line in METHODOLOGY.read_text(encoding="utf-8").splitlines()
            if line.startswith("speckit.spectra.domain-analyzer → ")
        )
        order = [part.strip().removeprefix("speckit.spectra.") for part in line.split("→")]
        self.assertEqual(order, FEEDERS)
        listed = [agent for agent in EXPECTED if agent in FEEDERS]
        self.assertEqual(listed, FEEDERS)


class TheSectionExplainsItself(unittest.TestCase):
    def test_it_recommends_declaring_the_artifact_root(self):
        for name, path in SURFACES.items():
            with self.subTest(surface=name):
                self.assertIn("Artifact root:", section(path))

    def test_it_says_why_the_constitution_runs_after_each_agent(self):
        for name, path in SURFACES.items():
            with self.subTest(surface=name):
                body = flat(section(path))
                self.assertIn("each later agent detects the constitution", body)
                self.assertIn("proposes only what it does not already say", body)

    def test_it_lies_outside_every_generated_region(self):
        for name, path in SURFACES.items():
            with self.subTest(surface=name):
                text = path.read_text(encoding="utf-8")
                at = text.index(f"{HEADING}</h2>" if path.suffix == ".html" else f"## {HEADING}")
                for start in (m.start() for m in re.finditer(r"<!-- SPECTRA:GENERATED START", text)):
                    end = text.index("<!-- SPECTRA:GENERATED END", start)
                    self.assertFalse(start < at < end, f"{name}: the section sits inside a generated region")


if __name__ == "__main__":
    unittest.main()
