# ctrl-01 secrets runtime protection

Purpose: describe an Ansible role that protects `control/secrets.vault.env` on the ctrl-01 node in line with ADR-0020, and supports both simple on-disk hardening and an optional in-memory projection model.

## Scope

- Applies to ctrl-01 and similar automation controllers that host `control/secrets.vault.env`.
- Assumes Azure Key Vault (AKV) is the primary source of truth for secrets, with `control/tools/helper/secrets` responsible for syncing into `control/secrets.vault.env`.
- Focuses on local runtime protection of the derived file only; it does not fetch or rotate secrets.

## Modes

### Mode 1 – on-disk hardening (baseline)

Baseline behaviour for workstations, lab nodes, and early ctrl-01 builds:

- Ensure `control/secrets.vault.env` exists with strict permissions (for example `0600`).
- Enforce owner and group aligned with the automation user (for example `ctrl01` or `jenkins` service account).
- Optionally assign a dedicated group (for example `hybridops-ops`) and restrict membership.
- Ensure the parent directory is not world-readable.

This mode keeps the file on disk but narrows access to the smallest practical set of users and services.

### Mode 2 – in-memory projection (planned)

Planned behaviour for production-like ctrl-01 deployments:

- Place the effective `secrets.vault.env` on a tmpfs-backed path (for example `/run/hybridops/secrets.vault.env`).
- Ensure `control/secrets.vault.env` is either:
  - a symlink or bind-mount to the tmpfs-backed file, or
  - a short-lived file that is removed once services have loaded their configuration.
- Integrate with systemd units where appropriate so secrets are materialised only when required by services (for example Jenkins, NetBox sync helpers) and removed or reloaded cleanly.

This mode reduces the exposure window for secrets on disk while remaining compatible with existing tooling that expects `control/secrets.vault.env` to be present.

## Integration points

- Runs after AKV sync has populated `control/secrets.vault.env` via `control/tools/helper/secrets/sync_from_akv.sh`.
- Intended to be invoked from the ctrl-01 bootstrap and hardening flows (for example as part of the `hybridops.apps` ctrl-01 / Jenkins controller roles).
- Can be applied idempotently during DR drills and regular maintenance to verify permissions and tmpfs configuration.

## Implementation notes

- Role tasks should be parameterised to allow selecting the mode (`on_disk` vs `tmpfs`) via variables, with `on_disk` as the default for labs.
- Any tmpfs configuration must be documented and validated by a dedicated runbook, including reboot behaviour and interaction with automation users.
- This README is a design reminder; detailed task structure and variables belong in the role's `README.md` and `defaults/main.yml` once implemented.
