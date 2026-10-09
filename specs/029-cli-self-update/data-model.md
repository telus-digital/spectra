# Data Model: Update the spectra Command From Anywhere

No persisted data. The command reads two facts and moves through a short, linear state machine.

## Entities

### Installed command

| Field | Source | Notes |
| --- | --- | --- |
| `installed` | `version.read_installed_version()` | Package metadata; falls back to the committed `VERSION` in a source tree. |
| `kind` | `version.classify_uninstall()` | `UV_MANAGED`, `PIP_OR_SOURCE`, `NOT_INSTALLED` (source checkout), `UNKNOWN_UV_ABSENT`. Read only when an update is available (research R2). |

### Newest release

| Field | Source | Notes |
| --- | --- | --- |
| `latest` | `version.check_update()["latest"]` | Highest bare-semver GitHub Release/tag; `None` when unreachable. |
| `status` | `version.check_update()["status"]` | `up_to_date`, `update_available`, `ahead`, `latest_unknown`. |

## State transitions

```text
start
  └─ check_update()
       ├─ latest_unknown ───────────────────────────────► UNREACHABLE      exit 3
       ├─ up_to_date | ahead ───────────────────────────► CURRENT          exit 0
       └─ update_available
            └─ classify_uninstall()
                 ├─ NOT_INSTALLED | PIP_OR_SOURCE ──────► NOT_UPDATABLE    exit 0
                 ├─ UNKNOWN_UV_ABSENT ─────────────────► UV_MISSING       exit 4
                 └─ UV_MANAGED
                      └─ show plan (installed → latest)
                           ├─ --yes ───────────────────┐
                           ├─ non-TTY, no --yes ───────┼──► REFUSED       exit 1
                           ├─ TTY, answered no ────────┼──► DECLINED      exit 1
                           └─ TTY, answered yes ───────┘
                                └─ perform_update(latest)
                                     ├─ UpdateError ───► FAILED           exit 4
                                     └─ ok ────────────► UPDATED          exit 0
```

Invariants:

- No state reads or writes anything under the current working directory (FR-002, FR-003).
- Every terminal state other than `UPDATED` leaves `installed` unchanged, and only `CURRENT` may say
  "up to date" (SC-005).
- `--no-update-check` / `SPECTRA_NO_UPDATE_CHECK` do not alter any transition (FR-011).
