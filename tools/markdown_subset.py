# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""The Markdown subset agent prose is written in, parsed and rendered to HTML with the standard library.

**Maintainer tooling. Not shipped.** Used by `tools/generate_agent_docs.py` to put the prose authored
in `agents/` onto the Agent reference page.

The subset is what the prose actually uses, and nothing more: paragraphs, `-` and `1.` lists nested
by indentation, fenced code with an optional info string, pipe tables, `##` headings, code spans,
`**bold**`, `*italic*`, `[links](url)` and backslash escapes. Everything else is refused with the line
it is on, rather than rendered approximately — GitHub renders `AGENTS_LIST.md` and this module renders
the website, and the two must agree on every construct the source contains.

Text is escaped before any markup is applied, and code-span contents are lifted out first so they
are never interpreted. Raw HTML in prose is refused, not escaped: GitHub would swallow `<word>` as a
tag while the website showed it, which is exactly the disagreement this module exists to prevent.
"""

from __future__ import annotations

import html
import re

BULLET = re.compile(r"^- (.*)$")
ORDERED = re.compile(r"^(\d+)\. (.*)$")
FENCE = re.compile(r"^```([A-Za-z0-9_+-]*)\s*$")
ENTITY = re.compile(r"&(#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")
RAW_TAG = re.compile(r"<[A-Za-z/!?]")
LINK = re.compile(r"\[([^\[\]]+)\]\(([^()\s]+)\)")
BOLD = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", re.S)
ITALIC = re.compile(r"(?<![*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![*\w])", re.S)
ESCAPABLE = "\\`*_[]()#+-.!|<>"

# Placeholders live in Unicode's private-use area, which never appears in authored prose.
PLACEHOLDER = 0xE000


class MarkdownError(Exception):
    """Something outside the subset. `line` is the 1-based source line, when known."""

    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line


# --------------------------------------------------------------------------- #
# Blocks
# --------------------------------------------------------------------------- #

class Paragraph:
    def __init__(self, lines, line):
        self.lines, self.line = lines, line

    @property
    def text(self):
        return "\n".join(self.lines)


class Code:
    def __init__(self, info, lines, line):
        self.info, self.lines, self.line = info, lines, line


class Table:
    def __init__(self, header, rows, line):
        self.header, self.rows, self.line = header, rows, line


class Heading:
    def __init__(self, text, line):
        self.text, self.line = text, line


class ListBlock:
    def __init__(self, ordered, start, items, line):
        self.ordered, self.start, self.items, self.line = ordered, start, items, line


def _indent(text):
    return len(text) - len(text.lstrip(" "))


def _marker(text):
    """(ordered, number, content_offset, rest) when `text` opens a list item at column 0, else None."""
    match = BULLET.match(text)
    if match:
        return False, None, 2, match.group(1)
    match = ORDERED.match(text)
    if match:
        return True, int(match.group(1)), len(match.group(1)) + 2, match.group(2)
    return None


def _starts_block(text):
    return (_marker(text) is not None or FENCE.match(text) is not None or text.startswith("#")
            or text.startswith("|") or text.startswith(">"))


def parse(lines, first_line=1):
    """Parse `lines` (strings, no newlines) into blocks; `first_line` is the source line of lines[0]."""
    numbered = [(first_line + offset, text.rstrip()) for offset, text in enumerate(lines)]
    return _blocks(numbered)


def _blocks(numbered):
    blocks = []
    i = 0
    while i < len(numbered):
        number, text = numbered[i]
        if not text.strip():
            i += 1
            continue
        if _indent(text):
            raise MarkdownError("unexpected indentation; indent only list-item continuations and "
                                "nested lists", number)
        if text.startswith(">"):
            raise MarkdownError("blockquotes are not in the supported Markdown subset", number)
        if text.startswith("#"):
            if not text.startswith("## ") or text.startswith("###"):
                raise MarkdownError("only `## ` headings are supported", number)
            blocks.append(Heading(text[3:].strip(), number))
            i += 1
            continue
        fence = FENCE.match(text)
        if fence:
            body = []
            i += 1
            while i < len(numbered) and numbered[i][1].strip() != "```":
                body.append(numbered[i][1])
                i += 1
            if i == len(numbered):
                raise MarkdownError("code fence is never closed", number)
            blocks.append(Code(fence.group(1), body, number))
            i += 1
            continue
        if text.startswith("```"):
            raise MarkdownError("a code fence's info string may only be a single word", number)
        if text.startswith("|"):
            i = _table(numbered, i, blocks)
            continue
        if _marker(text):
            i = _list(numbered, i, blocks)
            continue
        lines = [text]
        i += 1
        while i < len(numbered) and numbered[i][1].strip() and not _starts_block(numbered[i][1]):
            if _indent(numbered[i][1]):
                raise MarkdownError("unexpected indentation inside a paragraph", numbered[i][0])
            lines.append(numbered[i][1])
            i += 1
        blocks.append(Paragraph(lines, number))
    return blocks


def _cells(text, number):
    """Split a table row on unescaped pipes that are not inside a code span."""
    if not (text.startswith("|") and text.endswith("|")):
        raise MarkdownError("table rows must start and end with `|`", number)
    cells, current, in_code, i = [], "", False, 1
    body = text[1:-1]
    while i - 1 < len(body):
        char = body[i - 1]
        if char == "\\" and i < len(body):
            current += char + body[i]
            i += 2
            continue
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code:
            cells.append(current.strip())
            current = ""
        else:
            current += char
        i += 1
    cells.append(current.strip())
    return cells


def _table(numbered, i, blocks):
    start = numbered[i][0]
    rows = []
    while i < len(numbered) and numbered[i][1].startswith("|"):
        rows.append((numbered[i][0], _cells(numbered[i][1], numbered[i][0])))
        i += 1
    if len(rows) < 2 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1][1]):
        raise MarkdownError("a table needs a header row followed by a `| --- |` separator row", start)
    width = len(rows[0][1])
    for number, cells in rows:
        if len(cells) != width:
            raise MarkdownError(f"table row has {len(cells)} cells; the header has {width}", number)
    blocks.append(Table([(cell, start) for cell in rows[0][1]],
                        [[(cell, number) for cell in cells] for number, cells in rows[2:]], start))
    return i


def _list(numbered, i, blocks):
    ordered, start, _, _ = _marker(numbered[i][1])
    line = numbered[i][0]
    items = []
    while i < len(numbered):
        number, text = numbered[i]
        opened = _marker(text)
        if opened is None or opened[0] != ordered:
            break
        _, _, offset, rest = opened
        body = [(number, rest)]
        i += 1
        while i < len(numbered):
            next_number, next_text = numbered[i]
            if not next_text.strip():
                # A blank line continues the item only if indented content follows it.
                j = i
                while j < len(numbered) and not numbered[j][1].strip():
                    j += 1
                if j < len(numbered) and _indent(numbered[j][1]) >= offset:
                    body.extend((n, "") for n, _ in numbered[i:j])
                    i = j
                    continue
                break
            if _indent(next_text) >= offset:
                body.append((next_number, next_text[offset:]))
                i += 1
                continue
            if _indent(next_text):
                raise MarkdownError(f"list continuation must be indented {offset} spaces",
                                    next_number)
            break
        items.append(_blocks(body))
        # Blank lines between items keep the list going; anything else at column 0 ends it.
        j = i
        while j < len(numbered) and not numbered[j][1].strip():
            j += 1
        if j < len(numbered) and _marker(numbered[j][1]) and _marker(numbered[j][1])[0] == ordered:
            i = j
            continue
        break
    blocks.append(ListBlock(ordered, start, items, line))
    return i


# --------------------------------------------------------------------------- #
# Inline
# --------------------------------------------------------------------------- #

def inline_html(text, line=None):
    """Render one run of inline text (which may span lines) to HTML, refusing anything outside the subset."""
    stash = []

    def where(offset):
        return None if line is None else line + text.count("\n", 0, offset)

    def keep(fragment):
        stash.append(fragment)
        return chr(PLACEHOLDER + len(stash) - 1)

    out, i = [], 0
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text) and text[i + 1] in ESCAPABLE:
            out.append(keep(html.escape(text[i + 1])))
            i += 2
            continue
        if char == "`":
            run = len(text[i:]) - len(text[i:].lstrip("`"))
            end = -1
            for closer in re.finditer(r"`+", text[i + run:]):
                if len(closer.group(0)) == run:
                    end = i + run + closer.start()
                    break
            if end == -1:
                raise MarkdownError("code span is never closed", where(i))
            content = text[i + run:end].replace("\n", " ")
            if content.startswith(" ") and content.endswith(" ") and content.strip():
                content = content[1:-1]
            out.append(keep("<code>" + html.escape(content) + "</code>"))
            i = end + run
            continue
        out.append(char)
        i += 1
    plain = "".join(out)

    for pattern, problem in ((RAW_TAG, "raw HTML is not supported; put it in `backticks`"),
                             (ENTITY, "HTML entities are not supported; write the character itself"),
                             (re.compile(r"!\["), "images are not supported"),
                             (re.compile(r"\]\[|^\[[^\]]+\]:", re.M),
                              "reference-style links are not supported")):
        found = pattern.search(plain)
        if found:
            raise MarkdownError(problem, where(found.start()))

    escaped = html.escape(plain, quote=False)

    def link(match):
        label, url = match.group(1), html.unescape(match.group(2))
        if not (url.startswith(("https://", "http://", "#")) or ":" not in url):
            raise MarkdownError(f"link target {url!r} is not http(s), an anchor, or a relative path",
                                line)
        return f'<a href="{html.escape(url)}">{label}</a>'

    escaped = LINK.sub(link, escaped)
    escaped = BOLD.sub(r"<b>\1</b>", escaped)
    escaped = ITALIC.sub(r"<i>\1</i>", escaped)
    if "*" in escaped:
        raise MarkdownError("unmatched `*` or `**`; escape a literal asterisk as `\\*`",
                            where(plain.find("*")) if "*" in plain else line)
    if "[" in escaped and "](" in escaped:
        raise MarkdownError("malformed link", line)

    return re.sub("[-]", lambda m: stash[ord(m.group(0)) - PLACEHOLDER], escaped)


def check_inline(text, line=None):
    """Validate inline text without keeping the result."""
    inline_html(text, line)


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #

def to_html(blocks):
    """Block HTML for a parsed body fragment. Headings are rendered as `<h4>`."""
    parts = []
    for block in blocks:
        if isinstance(block, Paragraph):
            parts.append("<p>" + inline_html(block.text, block.line) + "</p>")
        elif isinstance(block, Heading):
            parts.append("<h4>" + inline_html(block.text, block.line) + "</h4>")
        elif isinstance(block, Code):
            attribute = f' class="language-{block.info}"' if block.info else ""
            parts.append(f"<pre><code{attribute}>" + html.escape("\n".join(block.lines), quote=False)
                         + "</code></pre>")
        elif isinstance(block, Table):
            head = "".join("<th>" + inline_html(cell, line) + "</th>" for cell, line in block.header)
            body = "".join("<tr>" + "".join("<td>" + inline_html(cell, line) + "</td>"
                                            for cell, line in row) + "</tr>" for row in block.rows)
            parts.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        elif isinstance(block, ListBlock):
            tag = "ol" if block.ordered else "ul"
            start = f' start="{block.start}"' if block.ordered and block.start != 1 else ""
            items = "".join("<li>" + _item_html(item) + "</li>" for item in block.items)
            parts.append(f"<{tag}{start}>{items}</{tag}>")
    return "".join(parts)


def _item_html(blocks):
    """A tight list item's leading paragraph renders without `<p>`, as browsers expect of a list."""
    if blocks and isinstance(blocks[0], Paragraph):
        return inline_html(blocks[0].text, blocks[0].line) + to_html(blocks[1:])
    return to_html(blocks)
