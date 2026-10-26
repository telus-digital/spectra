# Contract: Agent source file format

This is the format the maintainer writes. Anything not described here is rejected, with the file and
line named.

## Shipped Spectra agent: `agents/uat.md` (abridged; values illustrative)

````markdown
---
id: uat
title: UAT Runner
command: speckit.spectra.uat
provider: spectra
type: add-on
phase: testing-quality
order: 40
status: available
summary: Perform a feature's user-acceptance scenarios on the real build, after implementation and only when asked.
manifest: Perform the active feature's UAT scenarios on the real build — after implement, only when asked — and tick only what was seen to pass.
---

Perform a feature's user-acceptance scenarios on the real build — **after implementation, and only
when you ask**. …

It shows **the exact command** it would run to start the build and waits for your confirmation. …

## Arguments

none needed — it finds the feature the way the implement command does and names it before anything
starts. …

## Use it when

the UAT phase of `tasks.md` is open and you want the agent-drivable scenarios run with evidence.

## Where it writes

`uat-report.md` beside the spec, plus captures under `specs/<feature>/uat/<run-stamp>/`.

## Examples

```
/speckit-spectra-uat
/speckit-spectra-uat --env staging
/speckit-spectra-uat specs/021-signed-webhooks
```

## Change the shape of your UAT reports

The report's structure comes from `uat-report-template.md`. To use your own:

1. Copy it into `.specify/templates/overrides/`.
2. Edit it there and commit it.
````

## Header

- The first line is exactly `---`, and the header ends at the next line that is exactly `---`.
- Each line between them is `key: value`. The key is `[a-z]+`, and the value is everything after the
  first `": "`, trimmed. Values are literal: quotes, colons, `#` and `—` mean themselves.
- Keys, rules and the required/optional matrix are in [data-model.md](../data-model.md#agent-agentsidmd).
  A blank line, a comment line, or a repeated key inside the header is an error.

## Body (shipped agents only)

```text
lead paragraph                      required, inline formatting only
[further prose blocks]              optional
## Arguments                        required, one paragraph, optionally followed by one list
## Use it when                      required
[## <Label> …]                      optional items
## Examples                         required, exactly one fenced block, one invocation per line
[## <Guide title> …]                optional guides
```

- `##` is the only heading level. Position decides kind: a heading up to and including `Examples`
  is an item; one after `Examples` is a guide.
- An item label ending in `.`, `?` or `!` renders as `**Label.** text`; any other label renders as
  `**Label** — text`.
- The body of a non-shipped agent must be empty.

## Markdown subset

| Allowed | Notes |
| --- | --- |
| Paragraphs | Line breaks inside a paragraph are kept as written |
| `- ` bulleted lists | Nest by indenting two spaces under the parent's text |
| `1. ` ordered lists | Nest as above; numbers are emitted as written |
| Fenced code ```` ``` ```` | Optional info string (`bash`, `text`); contents are verbatim and escaped in HTML |
| Pipe tables | Header row, `---` separator row, then body rows; cells are inline-only |
| `` `code` `` | Contents are never interpreted |
| `**bold**`, `*italic*` | Rendered as `<b>` and `<i>` in HTML |
| `[text](url)` | `http://`, `https://`, `#anchor`, or a relative path |
| `\*`, `` \` ``, `\[`, `\\` | Backslash escapes |

| Rejected | Why |
| --- | --- |
| `#`, `###` and deeper headings | One heading level keeps structure positional |
| `>` blockquotes, images, reference links, footnotes | Not in use; each would need a renderer |
| `<` followed by a letter or `/` outside code | GitHub treats it as HTML; write it inside backticks |
| `&name;` and `&#…;` entities | Write the character itself |
| Unclosed `**`, `*`, `` ` `` or fence | Would render differently in each output |
| Other link schemes (`javascript:`, `data:` and so on) | Unsafe in the site's HTML |
