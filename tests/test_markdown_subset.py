"""The Markdown subset agent prose is written in (feature 040, research D5).

GitHub renders `AGENTS_LIST.md`; `tools/markdown_subset.py` renders the website. These tests pin the
subset both agree on, the escaping that keeps the website safe, and the refusals — each naming its
line — that keep the two renderings from disagreeing.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import markdown_subset as md  # noqa: E402


def render(text, first_line=1):
    return md.to_html(md.parse(text.split("\n"), first_line))


class Inline(unittest.TestCase):

    def test_bold_italic_and_code(self):
        self.assertEqual(md.inline_html("**bold** and *it* and `code`"),
                         "<b>bold</b> and <i>it</i> and <code>code</code>")

    def test_code_inside_bold(self):
        self.assertEqual(md.inline_html("**`speckit.spectra.adr`**"),
                         "<b><code>speckit.spectra.adr</code></b>")

    def test_code_span_contents_are_never_interpreted(self):
        self.assertEqual(md.inline_html("`**not bold** <tag> &amp;`"),
                         "<code>**not bold** &lt;tag&gt; &amp;amp;</code>")

    def test_a_longer_backtick_run_can_hold_a_shorter_one(self):
        self.assertEqual(md.inline_html("`` a `b` c ``"), "<code>a `b` c</code>")

    def test_triple_backticks_inside_a_single_backtick_span(self):
        self.assertEqual(md.inline_html("a ` ```suggestion ` block"),
                         "a <code>```suggestion</code> block")

    def test_text_is_escaped(self):
        self.assertEqual(md.inline_html("a & b > c"), "a &amp; b &gt; c")

    def test_links(self):
        self.assertEqual(md.inline_html("[docs](https://example.test/?a=1&b=2)"),
                         '<a href="https://example.test/?a=1&amp;b=2">docs</a>')
        self.assertEqual(md.inline_html("[up](../README.md)"), '<a href="../README.md">up</a>')
        self.assertEqual(md.inline_html("[here](#anchor)"), '<a href="#anchor">here</a>')

    def test_backslash_escapes(self):
        self.assertEqual(md.inline_html(r"5 \* 3"), "5 * 3")

    def test_emphasis_may_span_lines(self):
        self.assertEqual(md.inline_html("**one\ntwo**"), "<b>one\ntwo</b>")


class Blocks(unittest.TestCase):

    def test_paragraph_keeps_its_line_breaks(self):
        self.assertEqual(render("one\ntwo"), "<p>one\ntwo</p>")

    def test_nested_bulleted_list(self):
        self.assertEqual(render("- a\n  more\n  - b\n- c"),
                         "<ul><li>a\nmore<ul><li>b</li></ul></li><li>c</li></ul>")

    def test_ordered_list_with_three_space_continuation(self):
        self.assertEqual(render("1. one\n   still one\n2. two"),
                         "<ol><li>one\nstill one</li><li>two</li></ol>")

    def test_ordered_list_not_starting_at_one(self):
        self.assertIn('<ol start="3">', render("3. three\n4. four"))

    def test_fence_with_info_string_is_escaped(self):
        self.assertEqual(render("```bash\necho \"<hi>\" & done\n```"),
                         '<pre><code class="language-bash">echo "&lt;hi&gt;" &amp; done</code></pre>')

    def test_table(self):
        self.assertEqual(render("| A | B |\n| --- | --- |\n| `x|y` | **z** |"),
                         "<table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr>"
                         "<td><code>x|y</code></td><td><b>z</b></td></tr></tbody></table>")

    def test_heading(self):
        self.assertEqual(render("## Title"), "<h4>Title</h4>")


class Refusals(unittest.TestCase):
    """Each refusal names the source line, so the maintainer can go straight to it."""

    CASES = (
        ("raw HTML", "a <b>x</b>", "raw HTML"),
        ("entity", "a &mdash; b", "entities"),
        ("blockquote", "> quoted", "blockquotes"),
        ("deeper heading", "### Deeper", "only `## `"),
        ("top heading", "# Top", "only `## `"),
        ("unclosed bold", "**open", "unmatched"),
        ("unclosed code span", "`open", "never closed"),
        ("unclosed fence", "```\nnever", "never closed"),
        ("image", "![alt](x.png)", "images"),
        ("reference link", "[a][b]", "reference-style"),
        ("unsafe scheme", "[a](javascript:alert)", "not http(s)"),
        ("bad table", "| A |\n| B |", "separator"),
    )

    def test_each_is_refused_with_its_line(self):
        for name, text, phrase in self.CASES:
            with self.subTest(name):
                with self.assertRaises(md.MarkdownError) as caught:
                    render("ok\n\n" + text, first_line=40)
                self.assertIn(phrase, str(caught.exception))
                self.assertEqual(caught.exception.line, 42)


if __name__ == "__main__":
    unittest.main()
