# Contract: The Document

## Location

`<artifact-root>/DEPLOYMENT_STRATEGY.md` — flat in the root, no subfolder, no sequence number, rewritten
in place on a re-run (FR-034, FR-042). Root resolution: declared `Artifact root:` → publication check on
`docs/` → `docs/` (FR-035). No earlier location exists (research R6).

## Template

Name `deployment-strategy-template`; shipped at `spectra/templates/deployment-strategy-template.md`;
resolved: `.specify/templates/overrides/` → `.specify/presets/<id>/templates/` →
`.specify/extensions/spectra/templates/` → `.specify/templates/` → inline skeleton. First readable,
non-empty layer wins; honoured, not repaired; guidance comments and `[PLACEHOLDER]` tokens stripped;
path reported (FR-036, FR-037).

## Front matter (example shape)

```yaml
---
mode: brownfield
generated: 2026-10-15T14:02:11-07:00
template: .specify/extensions/spectra/templates/deployment-strategy-template.md
run: 1
deployables:
  - name: "web"
    root: "apps/web"
    class: service
  - name: "sdk"
    root: "packages/sdk"
    class: library
coverage_of_analysis: "64 of 212 files opened; the rest are application source outside the deploy path"
amendment_state: absent
clarification:
  asked: 5
  answered: 4
  questions:
    - n: 1
      ask: "where this project is hosted (confirmation)"
      recommended: "GKE, per k8s/overlays/"
      answer: "GKE; confirmed"
      disposition: answered
---
```

## Sections (default template, in order)

1. **Classification and evidence** — deployables, classes, mode, deciding and dissenting signals.
2. **Environments & promotion** — table (environment, proves, audience, deploy method, gate in) + one
   Mermaid flowchart bound to the table.
3. **Pipeline, artifact & traceability**
4. **Release & versioning**
5. **Data & schema change**
6. **Rollback & recovery**
7. **Operability & configuration**
8. **Conditional lenses** — only those the evidence warrants; otherwise one line saying none were.
9. **Open questions / confirmation items** — item, who answers, what it blocks.
10. **Recommendations summary** — table: # | lens | deployable | recommendation | provenance | re-run mark.
11. **Proposed constitution amendment** — state, clause, conflict, approval, items, how to apply.
12. **Sources consulted and coverage of analysis** — read/present, could not see, inputs (repository
    and referenced), the five answers, no-network and no-execution statements, known limitations.

Each lens section: applicability; current state (brownfield/mixed) with provenance; recommendation with
provenance; exact change where possible.

## Rules the command enforces regardless of template

- Exactly one provenance per claim: `verified` | `claimed` | `stated` | `convention` (FR-021).
- Absences cite the search (FR-022).
- No invented client/ops values; they go to open questions (FR-024).
- Operability stays high level (FR-019).
- No secret reproduced (FR-007).
- The diagram draws only what the environments table states (research R7).
