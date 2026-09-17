# `hybridops.app`

Application and platform service roles for HybridOps.

This collection contains the service roles that sit above the shared platform primitives in `hybridops.common`: NetBox, EVE-NG, GNS3, pgBackRest repository services, and Jenkins controller or agent delivery.

Role-level variables and assumptions are documented in each role's `README.md`. Broader operator guidance lives at [docs.hybridops.tech](https://docs.hybridops.tech).

## Scope

- Linux-hosted platform services used by HybridOps modules and blueprints.
- Application roles that can be reused directly when their documented inputs are satisfied.
- Service roles intended to be packaged and consumed from Galaxy rather than copied into each project.

## Roles

| Role | Purpose |
|------|---------|
| `containerlab` | Install and verify a pinned Containerlab runtime. |
| `containerlab_gui` | Run pinned Containerlab API and web GUI components. |
| `containerlab_healthcheck` | Verify runtime, KVM, images and deployed lab state. |
| `containerlab_lab` | Validate and operate native Containerlab topologies. |
| `containerlab_recovery` | Export and import guarded off-host recovery data. |
| `eveng` | Install and configure EVE-NG. |
| `gns3_healthcheck` | Validate a GNS3 server and its local compute runtime. |
| `gns3_images` | Install authorised QEMU and IOU images and register templates. |
| `gns3_lab_archive` | Export and restore GNS3 projects and writable node state. |
| `gns3_server` | Install and configure a remote GNS3 server. |
| `gns3_starter_lab` | Create a zero-image GNS3 teaching topology. |
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
