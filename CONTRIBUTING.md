# Contributing to `hybridops.app`

`hybridops.app` provides application and platform roles for HybridOps.Tech (for example Jenkins controller, RKE2 control-plane, NetBox, Moodle, and core platform services).

Design and release context is maintained in the HybridOps.Tech documentation site.

## Contribution scope

Appropriate changes include:

- New roles for platform or application services.
- Improvements to existing roles (variables, idempotency, hardening, resilience).
- Test improvements (role-local smoke tests, Molecule scenarios where applicable).
- Documentation updates (`README.md` and role-level README content).

Bug reports and feature requests are handled via GitHub issues and pull requests.

## Development workflow

### Local setup

Use versions compatible with `requirements.txt`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Change guidelines

- Keep roles focused and composable.
- Avoid environment-specific secrets, IPs, and hostnames.
- Prefer variables and documentation over hardcoded assumptions.
- Maintain idempotency wherever practical.

### Tests

Role-local smoke tests:

```bash
cd roles/<role_name>
ansible-playbook -i tests/inventory.example.ini tests/smoke.yml
```

Molecule (where defined):

```bash
cd roles/<role_name>
molecule test
```

Platform integration (via the harness):

```bash
# In galaxy-collections-harness
make workspace.clone
make collections.sync
make venv.refresh
make test ROLE=<role_name>
```

### Pull requests

Include:

- Summary of changes.
- Test evidence (smoke and/or Molecule and/or platform integration).
- Links to relevant documentation pages where applicable.

## Role structure expectations

Each role should provide:

- `roles/<role_name>/tests/smoke.yml`
- `roles/<role_name>/tests/inventory.example.ini`

Molecule scenarios are recommended when container orchestration or multi-node behaviour is involved.

## Security and secrets

- Do not commit secrets, tokens, client IDs, or passwords.
- Accept sensitive values via variables, Vault, or environment lookups.
- Avoid logging sensitive values into task output or evidence artefacts.
