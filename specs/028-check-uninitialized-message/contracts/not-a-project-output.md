# Contract: "not a Spec Kit project" output

**Applies to**: `spectra check`, `spectra version`, `spectra update`, `spectra uninstall`, when no
`.specify/` directory exists in the current folder or any parent.

## Standard output (ANSI styling removed)

```text
✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.
  Initialize Specify and add Spectra: spectra install
```

- Exactly these two lines from the state report, in this order.
- Line 2 starts with two spaces.
- `spectra install` is styled bold when colour is enabled; nothing else on line 2 is styled.
- The string `specify init` does not appear in the state report.

## Exit code

`EXIT_PROJECT_STATE` — unchanged from before this feature.

## Out of contract (unchanged)

- Start-of-run banner / update nudge printed by commands before the state check.
- `spectra install`'s own uninitialized-folder prompt and its manual `specify init` fallback.
