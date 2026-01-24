# `hybridops.app`

Application and platform roles for the HybridOps.Studio automation platform (for example Jenkins, RKE2, NetBox, Moodle, and core Linux/Windows services). Role-level usage, variables, and assumptions are documented in each role’s `README.md`.

High-level platform context is maintained at [docs.hybridops.studio](https://docs.hybridops.studio).

## Scope

- Platform and application services for lab and small-to-mid environments.
- Linux targets (for example Rocky Linux 9, Ubuntu 22.04+) and Windows Server targets (for example Windows Server 2022+), subject to role-level requirements.
- Roles are intended to be reusable outside HybridOps.Studio when inputs and dependencies are satisfied.

## Roles

| Role | Purpose |
|------|---------|
| `control_node_secrets_guard` | Apply runtime secrets protections on the automation control node. |
| `jenkins_controller` | Deploy Jenkins controller on the control node. |
| `linux_deploy_nginx` | Install and configure NGINX for web and reverse-proxy workloads. |
| `linux_rke2_install` | Install and configure RKE2 on Linux nodes. |
| `moodle_stack` | Deploy Moodle and supporting services. |
| `netbox_bootstrap` | Install NetBox and connect it to the required backend services. |
| `netbox_seed` | Seed NetBox with initial data (sites, VLANs, prefixes, device roles). |
| `rke2_controlplane` | Configure the RKE2 control-plane node(s). |
| `windows_configure_cluster` | Configure Windows Server clustering primitives where required. |
| `windows_domain_join` | Join Windows Server instances to Active Directory. |
| `windows_install_sql` | Install and configure Microsoft SQL Server. |
| `windows_windows_updates` | Configure Windows Update and patching baseline. |

## Requirements

- Ansible `ansible-core` 2.15+.
- Python 3.10+ on the control node.
- Supported targets depend on role requirements and documented variables.

## Installation

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install hybridops.app
```

Pin in `collections/requirements.yml`:

```yaml
collections:
  - name: hybridops.app
    version: ">=0.1.0"
```

## Usage

```yaml
- name: Bootstrap Jenkins controller on control node
  hosts: control_nodes
  become: true
  collections:
    - hybridops.app

  roles:
    - role: hybridops.app.jenkins_controller
```

## Testing

- Role-local smoke tests are provided under `roles/<role>/tests/` and exercised against a lab inventory.
- Molecule scenarios may be provided where isolated validation is valuable.
- Platform integration tests are executed via HybridOps.Studio pipelines and lab inventories.

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)  
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/)
for project-wide licence details, including branding and trademark notes.
