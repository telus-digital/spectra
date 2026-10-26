# Contract: Agent reference page markup

`docs/getting-started/agents.html` keeps its current structure. The sidebar and the card list become
generated regions. The CSS, the scroll-spy script, and the copy buttons depend on the class names
below, and so do the flow tests (`test_adr_flow`, `test_uat_flow`, `test_test_plan_flow`). Changing
any of them is a breaking change to this contract.

## Sidebar (`agents-page-nav`, inside `<nav class="scen-nav-track">`)

```html
<a href="#a-<id>"><span class="n">NN</span><span class="t"><title><small><id></small></span></a>
```

One link per shipped agent, in roster order. `NN` is the two-digit number.

## Card (`agents-page-cards`, inside `<ul class="cmds">`)

```html
<li class="agent" id="a-<id>">
  <header><span class="n">NN</span><h3><title></h3><span class="phase"><phase title></span></header>
  <span class="name"><command></span>
  <span class="cdesc"><lead, inline HTML only></span>
  <div class="args"><b>Arguments:</b> <Arguments paragraph, inline HTML>[<ul>…</ul>]</div>
  <span class="lbl">Example (Claude)</span>          <!-- "Examples (Claude)" when > 1 line -->
  <pre><code><example line 1></code></pre>
  <pre><code><example line 2></code></pre>
  <details class="fullref">
    <summary>Full reference</summary>
    <div class="fullref-body"><full body as block HTML></div>
  </details>
</li>
```

Invariants the tests rely on:

1. `.cdesc` contains only `<b>`, `<i>`, `<code>` and `<a>`, never a `<span>`. A test reads from
   `class="cdesc"` to the next `</span>`. `.args` is a `<div>` so that an Arguments list (create-pr,
   review-pr) can follow its paragraph; it contains no `<span>` either.
2. The first `<pre><code>` in a card holds exactly the first example line.
3. The `<details>` block comes after every example. Lists inside it may contain `<li>`, so tests that cut
   a card at the first `</li>` still see the lead, arguments and examples intact.
4. All text is HTML-escaped. Typographic characters are written as characters, not entities.
5. The page renders fully with scripts disabled. `<details>` opens natively.

## Full reference body (block HTML)

| Source | HTML |
| --- | --- |
| Lead and paragraphs | `<p>` |
| Lists | `<ul>`/`<ol>` with nested lists inside `<li>` |
| Code fence | `<pre><code>` (with `class="language-<info>"` when an info string is present) |
| Table | `<table><thead>…</thead><tbody>…</tbody></table>` |
| Items | `<ul class="items"><li><b>Label</b> — …</li></ul>`, using the same joiner rule as Markdown |
| Guides | `<h4>` followed by its blocks |

`getting-started.css` gains styles for `details.fullref`, `.fullref-body` and `ul.items`. Nothing else
in the stylesheet changes.
