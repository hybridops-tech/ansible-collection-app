# Contributing to `hybridops.app`

`hybridops.app` provides application and platform roles used by the HybridOps
runtime.

## Contribution scope

Appropriate changes include:

- New roles for platform or application services.
- Improvements to existing roles (variables, idempotency, hardening, resilience).
- Test improvements (role-local smoke tests, Molecule scenarios where applicable).
- Documentation updates (`README.md` and role-level README content).

Bug reports and feature requests are handled through the documented HybridOps support and maintainer workflow.

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

Changes that affect Core operations must also pass the relevant
[`hybridops-core`](https://github.com/hybridops-tech/hybridops-core) checks.

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

Report vulnerabilities through the [security
policy](SECURITY.md), not a public issue.
