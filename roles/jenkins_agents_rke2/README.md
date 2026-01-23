# Role: jenkins_agents_rke2

Configure Jenkins **Kubernetes (RKE2) pod agents** using Jenkins Configuration as Code (JCasC).

This role assumes a Jenkins controller is already deployed on the control node
(for example `ctrl-01`) using `hybridops.app.jenkins_controller`, aligned with
[ADR-0603 – Run Jenkins controller on control node, agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-jenkins-controller-docker-agents-rke2/).

The purpose of this role is to define an **RKE2-backed Kubernetes cloud** and at
least one **pod template** so pipeline workload executes on Kubernetes rather
than on the controller.

---

## What this role does

- Renders a JCasC fragment into the controller `JENKINS_HOME` volume under
  `casc_configs/` (for example `casc_configs/20-agents-rke2.yaml`).
- Defines (via JCasC):
  - A Kubernetes cloud (default name: `rke2`).
  - A default pod template using a tooling-capable agent image (Terraform,
    kubectl, Helm, Ansible, etc).
  - A credential (bearer token) used by the Jenkins Kubernetes plugin to
    create/delete agent pods.
- Optionally restarts the controller container to apply the new configuration
  (recommended for deterministic convergence).

---

## What this role does not do

- It does **not** install RKE2.
- It does **not** install Prometheus / monitoring stacks on Kubernetes.
- It does **not** require Script Console access (`/scriptText`).
- It does **not** assume any specific secret store. Provide tokens via inventory,
  Vault, or your organisation’s secret workflow.

---

## Requirements

### Controller host

- Jenkins controller is deployed and healthy on the target host.
- Controller is configured to load JCasC from `JENKINS_HOME/casc_configs/`.
  (This is typically handled by the `jenkins_controller` role templates.)

### Jenkins controller plugins

- Jenkins **Kubernetes plugin** is installed on the controller.

### Kubernetes/RKE2

- Kubernetes API endpoint reachable from the controller host.
- An RBAC token that can manage pods in the agent namespace. At minimum:
  `create`, `delete`, `get`, `list`, `watch` on pods (and typically pods/log,
  pods/exec depending on your pipelines).

---

## Security considerations

- Treat the Kubernetes bearer token as a high-value secret.
- Prefer namespaced RBAC (least privilege) over cluster-admin tokens.
- Avoid printing credentials in logs. This role should keep secrets out of stdout.

---

## Key variables

Defaults are defined in `defaults/main.yml`. Common variables:

- `jenkins_agents_rke2_server_url`  
  Kubernetes API endpoint used by Jenkins Kubernetes plugin (required).

- `jenkins_agents_rke2_namespace`  
  Namespace where agent pods will run (required).

- `jenkins_agents_rke2_bearer_token`  
  Bearer token for Kubernetes API access (required; provide via inventory/Vault).

- `jenkins_agents_rke2_agent_image`  
  Tooling image for the pod template (for example `hybridops/ci-agent-tools:0.1.0`).

- `jenkins_agents_rke2_cloud_name`  
  Jenkins cloud name (default: `rke2`).

- `jenkins_agents_rke2_restart_controller`  
  Restart controller container after rendering JCasC (recommended).

> Note: If your controller role already defines additional agent templates or
> credentials via JCasC fragments, ensure filenames and ordering are consistent
> (e.g. `20-*.yaml`, `30-*.yaml`, `40-*.yaml`) so config loads predictably.

---

## Example

```yaml
- name: Configure RKE2 pod agents for Jenkins controller
  hosts: ctrl_nodes
  become: true
  gather_facts: true

  collections:
    - hybridops.app

  vars:
    jenkins_agents_rke2_server_url: "https://10.10.0.10:6443"
    jenkins_agents_rke2_namespace: "ci-agents"
    jenkins_agents_rke2_bearer_token: "{{ vault_rke2_jenkins_token }}"
    jenkins_agents_rke2_agent_image: "hybridops/ci-agent-tools:0.1.0"
    jenkins_agents_rke2_restart_controller: true

  roles:
    - role: hybridops.app.jenkins_agents_rke2
```

---

## Validation

After the role runs:

1. Jenkins loads without JCasC boot errors.
2. In Jenkins, a pipeline targeting the RKE2 label schedules onto a pod agent.

Example pipeline snippet:

```groovy
pipeline {
  agent { label 'rke2' }
  stages {
    stage('proof') {
      steps {
        sh 'whoami && terraform version | head -n 1'
      }
    }
  }
}
```

---

## License

- Code: MIT-0  
- Documentation: CC BY 4.0
