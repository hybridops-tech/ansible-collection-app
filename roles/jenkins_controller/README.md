# jenkins_controller

Deploy a Jenkins controller on a Linux control node using Docker Compose v2, with controller-only defaults and Configuration as Code (JCasC).

## Summary

- Builds a custom Jenkins controller image from `jenkins/jenkins:lts` with a pinned plugin set.
- Deploys the controller as a Docker Compose stack on the target host.
- Renders baseline JCasC into the Jenkins home volume.
- Optionally manages a Jenkins admin API token for automation.
- Optionally seeds a minimal bootstrap credential set via JCasC (disabled by default).

Design context: [ADR-0603 – Run Jenkins controller on control node, agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-jenkins-controller-docker-agents-rke2/).

## Requirements

- Ansible 2.15+
- Python 3.10+ on the target host
- Docker Engine and Docker Compose v2 installed and reachable via `docker`
- Supported targets: Ubuntu 22.04+, Rocky Linux 9+

## Role variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Notes |
|---|---:|---|
| `jenkins_image` | `jenkins/jenkins` | Base image for controller build. |
| `jenkins_version` | `lts` | Base tag and controller tag. |
| `jenkins_home_path` | `/opt/jenkins` | Host directory for Jenkins data and config. |
| `jenkins_uid` / `jenkins_gid` | `1000` / `1000` | Ownership for the mounted Jenkins home. |
| `jenkins_http_port` | `8080` | Internal container HTTP port. |
| `jenkins_external_http_port` | `8080` | Host port for HTTP. |
| `jenkins_agent_port` | `50000` | Internal container agent port. |
| `jenkins_external_agent_port` | `50000` | Host port for agent traffic. |
| `jenkins_controller_image` | `hybridops/jenkins-controller` | Built image name. |
| `jenkins_container_name` | `jenkins-controller` | Compose service/container name. |
| `jenkins_network_name` | `jenkins` | Docker network for the controller. |
| `jenkins_controller_num_executors` | `0` | Controller-only pattern. |
| `jenkins_enable_healthcheck` | `true` | Wait for HTTP readiness. |
| `jenkins_build_timeout` | `900` | Build timeout for first run. |
| `jenkins_admin_username` | `admin` | Admin user in JCasC baseline. |
| `jenkins_admin_password` | `""` | Required. Provide via inventory/secret store. |

## JCasC outputs

Rendered under:

- `{{ jenkins_home_path }}/jenkins_home/casc_configs/00-controller.yaml`
- `{{ jenkins_home_path }}/jenkins_home/casc_configs/20-credentials.yaml` (optional)
- `{{ jenkins_home_path }}/jenkins_home/casc_configs/30-nodes-docker.yaml` (optional)
- `{{ jenkins_home_path }}/jenkins_home/casc_configs/40-prometheus.yaml` (optional)

## Admin API token management

When enabled, ensures an admin API token exists on the controller host for automation.

- If `jenkins_admin_api_token` is set, it is used (and persisted if missing).
- Else if the token file exists, it is loaded.
- Else a token is minted via the Jenkins HTTP API and persisted.

Key variables:

- `jenkins_bootstrap_api_token_enabled` (default: `false`)
- `jenkins_admin_api_token_file` (default: `{{ jenkins_home_path }}/.secrets/admin_api_token`)
- `jenkins_admin_api_token_name` (default: `hybridops-ansible`)
- `jenkins_bootstrap_api_token_force_rotate` (default: `false`)
- `jenkins_bootstrap_api_token_print_once` (default: `false`)

## JCasC bootstrap credentials

Optional bootstrap-only seeding via JCasC. Disabled by default.

### Supported credentials

- `ansible-vault-password` (string)
  - Seeded when `jenkins_ansible_vault_password` is non-empty.
- `gcp-runner-sa` (file)
  - Seeded when `jenkins_casc_secrets_enabled=true`.
  - Imported from a staged file under the Jenkins home volume.

### Variables

- `jenkins_ansible_vault_password` (default: empty)
- `jenkins_casc_secrets_enabled` (default: `false`)
- `jenkins_casc_secrets_stage` (default: `false`)
- `jenkins_gcp_runner_sa_key_src` (default: empty)
- `jenkins_casc_secrets_cleanup` (default: `false`)
- `jenkins_casc_secrets_delete_staged` (default: `true`)

### File staging and import

When enabled, the role stages the key file to:

- Host: `{{ jenkins_home_path }}/jenkins_home/casc_secrets/gcp/ci-runner-sa.json`
- Container: `/var/jenkins_home/casc_secrets/gcp/ci-runner-sa.json`

JCasC reads the file and stores it as a Jenkins file credential.

### Security notes

- Treat the Jenkins home volume as sensitive.
- Deleting the staged file does not remove the credential from Jenkins; it only reduces on-disk exposure.
- Keep bootstrap seeding minimal and use an external secrets strategy for steady state.

## Dependencies

None declared in `meta/main.yml`. Docker Engine and Docker Compose v2 must be installed before running this role.

## Example playbook

```yaml
- name: Deploy Jenkins controller
  hosts: ctrl_nodes
  become: true
  gather_facts: true

  roles:
    - role: jenkins_controller
      vars:
        jenkins_home_path: /opt/jenkins
        jenkins_external_http_port: 8080
        jenkins_admin_username: admin
        jenkins_admin_password: "{{ lookup('ansible.builtin.env', 'JENKINS_ADMIN_PASSWORD') }}"
        jenkins_enable_healthcheck: true
```

### Example: seed bootstrap credentials (optional)

```yaml
- name: Deploy Jenkins controller with bootstrap credentials
  hosts: ctrl_nodes
  become: true
  gather_facts: true

  roles:
    - role: jenkins_controller
      vars:
        jenkins_admin_password: "{{ lookup('ansible.builtin.env', 'JENKINS_ADMIN_PASSWORD') }}"
        jenkins_ansible_vault_password: "{{ lookup('ansible.builtin.env', 'ANSIBLE_VAULT_PASSWORD') }}"
        jenkins_casc_secrets_enabled: true
        jenkins_casc_secrets_stage: true
        jenkins_gcp_runner_sa_key_src: "{{ lookup('ansible.builtin.env', 'JENKINS_GCP_RUNNER_SA_KEY_SRC') }}"
        jenkins_casc_secrets_cleanup: true
```

## Project context

HybridOps.Studio platform automation reference implementation: [docs.hybridops.studio](https://docs.hybridops.studio/).

## License

- Code: [MIT-0](https://spdx.org/licenses/MIT-0.html)
- Documentation & diagrams: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

HybridOps.Studio licensing and trademark notes: [Licensing](https://docs.hybridops.studio/briefings/legal/licensing/).
