# hybridops.app – Platform and application roles

Application and platform roles for the HybridOps.Studio automation platform.  
The collection focuses on end-to-end components such as Jenkins, RKE2, NetBox, Moodle, and core Linux/Windows services.

The collection is designed to be reusable outside HybridOps.Studio and can be consumed from Ansible Galaxy in projects that need opinionated, lab-ready roles for common platform services.

---

## 1. Collection scope

**Collection name:** `hybridops.app`  
**Galaxy collection (namespace.name):** `hybridops.app` (namespace `hybridops`, name `app`; publication planned)  
**Source repository:** [github.com/hybridops-studio/ansible-collection-app](https://github.com/hybridops-studio/ansible-collection-app)

Target environments:

- Linux application hosts (Rocky Linux, Ubuntu) for control-plane and application services.
- Windows Server hosts for hybrid workloads (SQL Server, domain join, updates).
- Control nodes and RKE2 cluster nodes that orchestrate the wider platform.

The main HybridOps.Studio platform repository consumes this collection under `deployment/` playbooks, but the collection can be installed and used in isolation.

---

## 2. Roles

Current roles:

| Role name                     | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| `control_node_secrets_guard`  | Apply runtime secrets protections on the automation control node.      |
| `jenkins_controller`          | Deploy Jenkins controller on the control node (Docker or systemd).     |
| `linux_deploy_nginx`          | Install and configure NGINX for web and reverse-proxy workloads.       |
| `linux_rke2_install`          | Install and configure RKE2 on Linux nodes.                             |
| `moodle_stack`                | Deploy Moodle and supporting services for the Academy lab.             |
| `netbox_bootstrap`            | Install NetBox and connect it to the shared PostgreSQL backend.        |
| `netbox_seed`                 | Seed NetBox with sites, VLANs, prefixes, and initial device roles.     |
| `rke2_controlplane`           | Configure the RKE2 control-plane node(s).                              |
| `windows_configure_cluster`   | Configure Windows Server clustering primitives where required.         |
| `windows_domain_join`         | Join Windows Server instances to Active Directory.                     |
| `windows_install_sql`         | Install and configure Microsoft SQL Server.                            |
| `windows_windows_updates`     | Configure Windows Update and patching baseline.                        |

Role-level READMEs document parameters, inputs, and expected host facts where needed.

---

## 3. Requirements

- Ansible **2.15+** (or the long-term supported version selected for HybridOps.Studio).
- Python **3.10+** on the control node.
- Supported target systems:
  - Rocky Linux 9 and Ubuntu 22.04+ for Linux roles.
  - Windows Server 2022+ for Windows roles (WinRM enabled and reachable).

Collection requirements and supported versions are also tracked in `galaxy.yml`.

---

## 4. Installation and usage

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install hybridops.app
```

Or via `collections/requirements.yml`:

```yaml
collections:
  - name: hybridops.app
    version: "*"
```

Example playbook:

```yaml
- name: Bootstrap Jenkins controller on control node
  hosts: control_nodes
  become: true
  collections:
    - hybridops.app

  roles:
    - role: hybridops.app.jenkins_controller
```

Combined usage with multiple roles:

```yaml
- name: Bring up core platform services
  hosts: control_nodes
  become: true
  collections:
    - hybridops.app

  roles:
    - role: hybridops.app.linux_rke2_install
    - role: hybridops.app.netbox_bootstrap
    - role: hybridops.app.jenkins_controller
```

---

## 5. Testing and CI

Roles in this collection use a mix of:

- **Self-contained tests** under `tests/` (for example `tests/inventory.example.ini` and `tests/smoke.yml`) to exercise the role in isolation.
- **Molecule scenarios** under `molecule/default/` for roles that benefit from container- or lab-based validation.
- **Platform integration tests** in the HybridOps.Studio platform and collections workspaces, where playbooks under `deployment/` and CI pipelines exercise the collection end to end against real VMs.

A repository-level `Makefile` provides a thin wrapper around Molecule:

- `make test` runs `molecule test` for all roles that have a `molecule/default/` scenario.
- `make test ROLE=jenkins_controller` runs `molecule test` for a single role.

This keeps role testing self-contained while proving the collection in realistic CI workflows.

---

## 6. Relationship to the HybridOps.Studio platform

This collection is maintained as part of the HybridOps.Studio project.  
The main platform repository (`hybridops-platform`) consumes `hybridops.app` from Galaxy and wires the roles into higher-level scenarios, including:

- Control-plane bootstrap and refresh.
- NetBox as source of truth with shared PostgreSQL.
- RKE2 platform bring-up.
- Academy workloads such as Moodle.

Architecture decisions, runbooks, and evidence for these scenarios are documented in the HybridOps.Studio documentation site and ADR index in the main platform repository.

---

## 7. Development

Repository layout (simplified):

```text
ansible_collections/hybridops/app/
├── roles/
│   ├── control_node_secrets_guard/
│   ├── jenkins_controller/
│   ├── linux_deploy_nginx/
│   ├── linux_rke2_install/
│   ├── moodle_stack/
│   ├── netbox_bootstrap/
│   ├── netbox_seed/
│   ├── rke2_controlplane/
│   ├── windows_configure_cluster/
│   ├── windows_domain_join/
│   ├── windows_install_sql/
│   └── windows_windows_updates/
├── plugins/
└── README.md
```

Practices:

- Each role maintains its own `defaults/`, `vars/`, `tasks/`, handlers, and README.
- Integration and scenario tests (including Molecule where used) live alongside roles under their `tests/` or `molecule/` directories.

---

## 8. Releases

This collection is versioned with Semantic Versioning and published to Ansible Galaxy as `hybridops.app`.

Contribution guidelines are documented in `CONTRIBUTING.md` in this repository.

For maintainers, the end-to-end release workflow (versioning, changelog updates, build, publish and evidence capture) follows the standard HybridOps.Studio collections process described in ADR-0606:

- [ADR-0606 – Ansible collections release process](https://docs.hybridops.studio/adr/ADR-0606-ansible-collections-release-process/)

---

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
