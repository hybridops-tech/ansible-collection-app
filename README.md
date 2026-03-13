# `hybridops.app`

Application and platform service roles for HybridOps.

This collection contains the service roles that sit above the shared platform primitives in `hybridops.common`: NetBox, EVE-NG, pgBackRest repository services, and Jenkins controller or agent delivery.

Role-level variables and assumptions are documented in each role's `README.md`. Broader operator guidance lives at [docs.hybridops.tech](https://docs.hybridops.tech).

## Scope

- Linux-hosted platform services used by HybridOps modules and blueprints.
- Application roles that can be reused directly when their documented inputs are satisfied.
- Service roles intended to be packaged and consumed from Galaxy rather than copied into each project.

## Roles

| Role | Purpose |
|------|---------|
| `eveng` | Install and configure EVE-NG. |
| `jenkins_agents_docker` | Configure Docker-based Jenkins agents. |
| `jenkins_controller` | Install and configure Jenkins controller. |
| `netbox_service` | Install and operate NetBox service. |
| `pgbackrest_repo` | Install and configure pgBackRest repository service. |

## Requirements

- Ansible `ansible-core` 2.15+
- Python 3.10+ on the control node
- Supported target OS depends on the role

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
- name: Install NetBox
  hosts: netbox_hosts
  become: true
  collections:
    - hybridops.app

  roles:
    - role: hybridops.app.netbox_service
```

## Testing

- Role-local smoke and Molecule scenarios are included where they add value.
- Integration validation is exercised through HybridOps module and blueprint runs in `hybridops-core`.

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)
- Documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

See the project licensing guidance at [docs.hybridops.tech](https://docs.hybridops.tech).
