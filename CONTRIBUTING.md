# Contributing to `hybridops.app`

`hybridops.app` provides application and platform roles for HybridOps.Studio, including:

- Jenkins controller
- RKE2 control-plane
- NetBox
- Moodle
- Core Linux and Windows platform services

The goals are:

- Easy reuse in other environments.
- Strong test coverage (role-local, Molecule, and platform integration).
- A clear evidence story for CI and releases.

For broader context, see:

- ADR-0606 – Ansible collections release process (on the HybridOps.Studio docs site).
- The “Ansible collections and roles” index page in the documentation.

---

## 1. Contribution scope

Good contributions include:

- New roles for platform or application services.
- Enhancements to existing roles (variables, idempotency, hardening, resilience).
- Improvements to tests (role-local `tests/`, Molecule scenarios).
- Documentation updates in this collection’s `README.md` and role-level READMEs.

Bug reports and feature requests are handled via GitHub issues and pull requests.

---

## 2. Development workflow

1. **Fork and branch**

   - Fork the repository.
   - Create a topic branch: `feature/<short-description>` or `fix/<short-description>`.

2. **Local setup**

   - Use a Python and `ansible-core` version compatible with `requirements.txt`.
   - Install dependencies:

     ```bash
     python3 -m venv .venv
     . .venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Make your change**

   - Keep roles focused and composable.
   - Avoid environment-specific secrets, IPs, and hostnames.
   - Prefer variables and documentation over hardcoded assumptions.
   - Maintain idempotency wherever practical.

4. **Run tests**

   **Role-local smoke tests:**

   ```bash
   cd ansible_collections/hybridops/app/roles/<role_name>
   ansible-playbook -i tests/inventory.example.ini tests/smoke.yml
   ```

   **Molecule (where defined):**

   ```bash
   cd ansible_collections/hybridops/app/roles/<role_name>
   molecule test
   ```

   **Integration (from the shared collections workspace):**

   ```bash
   # In ansible-galaxy-hybridops
   make venv.refresh
   make test ROLE=<role_name>
   ```

5. **Open a pull request**

   - Describe what changed and why.
   - Explain how you tested it (smoke/Molecule/integration).
   - Reference any relevant ADRs, HOWTOs, or runbooks if applicable.

---

## 3. Role structure and testing expectations

Each public role should:

- Provide a **role-local test harness** under `roles/<role_name>/tests/`:
  - `tests/smoke.yml` – focused playbook exercising core behaviour.
  - `tests/inventory.example.ini` – example inventory for a small lab.
- Consider a **Molecule scenario** when:
  - The role manages containers (for example Jenkins on Docker).
  - Multi-node orchestration or more complex flows are involved.

Roles are expected to work in:

- Local/lab environments.
- Integration tests in the HybridOps platform (generic VMs and CI).

---

## 4. Style and quality

- Follow Ansible best practices (idempotency, meaningful variables, no secrets in code).
- Align variable names and patterns with existing roles in this collection.
- Keep comments minimal and focused on non-obvious intent.
- Use the tooling defined in `requirements.txt` (for example `ansible-lint`, Molecule) and any configured pre-commit hooks before opening a pull request.

---

## 5. Security and secrets

- **Never** commit real secrets, tokens, client IDs, or passwords.
- Use example values and clearly mark them as placeholders.
- Accept sensitive values via variables, vaults, or environment lookups — not hardcoded defaults.
- Avoid logging secrets into task output or evidence artefacts.

If in doubt, keep the role generic, documented, and safe to run in a shared lab.
