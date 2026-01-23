---
title: "HOWTO – Configure Jenkins Agents on RKE2"
category: "platform"
summary: >
  Configure Jenkins to execute pipeline workload on labelled Kubernetes pod agents in RKE2,
  while keeping the controller on ctrl-01 in controller-only mode. Agent configuration is
  expressed as JCasC and rendered into the controller volume for repeatable, governed runs.
difficulty: "Intermediate"
topic: "platform-jenkins-agents-rke2"
video: ""
source: ""
draft: false
is_template_doc: false
tags: ["jenkins", "cicd", "rke2", "kubernetes", "jcasc", "platform"]
access: academy

stub:
  enabled: true
  blurb: |
    Configure Jenkins to offload build execution to Kubernetes pod agents in RKE2.
    The controller remains on ctrl-01 (controller-only pattern), and pipelines target
    labelled pod templates rather than running on the controller host.

    This HOWTO establishes the Kubernetes cloud definition, pod templates, and validation
    signals so agent lifecycle is repeatable and suitable for evidence capture.
  highlights:
    - "Controller stays executor-less by default; build work runs on pod agents."
    - "Kubernetes cloud and pod templates are managed via JCasC and committed to Git."
    - "Validate pod lifecycle: create → connect → run → teardown."
  cta_url: "https://academy.hybridops.studio/courses/platform/jenkins-agents-rke2"
  cta_label: "Open the full Academy HOWTO"
---

# HOWTO – Configure Jenkins Agents on RKE2

**Purpose:** Configure Jenkins so CI workloads execute on **RKE2 pod agents** (steady state), while the controller remains on `ctrl-01` in **controller-only mode** (0 executors by default).

---

## Demo

- Demo video: *(add when available)*  
- Source: [Role: `hybridops.app.jenkins_agents_rke2`](https://github.com/hybridops-studio/ansible-collection-app/tree/main/roles/jenkins_agents_rke2)

??? info "▶ Show embedded demo (optional)"

    Replace `VIDEO_ID` when available.

    <iframe
      width="100%"
      height="400"
      src="https://www.youtube.com/embed/VIDEO_ID"
      title="HOWTO – Configure Jenkins Agents on RKE2 – HybridOps.Studio"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen>
    </iframe>

    If the embed does not load: [Open on YouTube](https://www.youtube.com/watch?v=VIDEO_ID){ target=_blank rel="noopener" }

---

## Prerequisites

- Jenkins controller deployed on `ctrl-01` via `hybridops.app.jenkins_controller` and healthy on the published HTTP port.
- Controller loads JCasC from a **directory** (recommended):
  - `CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs`
  - This is typically handled by the controller role template (Docker Compose env).
- RKE2 cluster reachable from `ctrl-01`:
  - Kubernetes API server URL and CA are known.
  - Network path is open (TCP 6443 or your API port).
- A Kubernetes namespace for agent pods (example: `ci-agents`).
- A Kubernetes service account with RBAC allowing Jenkins to manage agent pods in that namespace.

> **Design note:** The JCasC fragments in this HOWTO are ordered by a numeric prefix (for example `35-cloud-rke2.yaml`) so load order is deterministic when Jenkins reads the `casc_configs/` directory.

---

## Overview

This HOWTO uses `hybridops.app.jenkins_agents_rke2` to render:

- A JCasC fragment that defines:
  - A Kubernetes cloud (example name: `rke2`)
  - One or more pod templates with labels (example label: `rke2-infra`)
  - Credentials for Jenkins to authenticate to the Kubernetes API (bearer token + CA)

Optionally, the role restarts the controller container so the new configuration is applied immediately.

---

## Steps

### 1) Prepare the namespace and RBAC in RKE2

Create the namespace and service account:

```bash
kubectl create namespace ci-agents
kubectl -n ci-agents create serviceaccount jenkins-agent
```

Apply a minimal Role/RoleBinding (adjust to your policy):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: jenkins-agent
  namespace: ci-agents
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "pods/exec", "secrets", "configmaps"]
    verbs: ["get", "list", "watch", "create", "delete", "patch", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: jenkins-agent
  namespace: ci-agents
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: jenkins-agent
subjects:
  - kind: ServiceAccount
    name: jenkins-agent
    namespace: ci-agents
```

Apply it:

```bash
kubectl apply -f rbac-jenkins-agent.yaml
```

### 2) Obtain a service account token

How you mint tokens depends on your cluster version/policy. Example:

```bash
kubectl -n ci-agents create token jenkins-agent
```

Store the token in your secret system (Vault/AKV/etc). Treat it as high-privilege.

### 3) Apply the role on `ctrl-01`

Example playbook:

```yaml
- name: Configure Jenkins RKE2 pod agents (JCasC)
  hosts: ctrl_nodes
  become: true
  gather_facts: true

  collections:
    - hybridops.app

  vars:
    jenkins_home_path: "/opt/jenkins"

    jenkins_agents_rke2_server_url: "https://rke2-api.example.internal:6443"
    jenkins_agents_rke2_namespace: "ci-agents"

    # Provide via Vault/secret store
    jenkins_agents_rke2_bearer_token: "{{ vault_rke2_jenkins_bearer_token }}"
    jenkins_agents_rke2_ca_crt_b64: "{{ vault_rke2_ca_crt_b64 }}"

    # Pod template baseline
    jenkins_agents_rke2_agent_label: "rke2-infra"
    jenkins_agents_rke2_agent_image: "hybridops/ci-agent-tools:0.1.0"

  roles:
    - role: hybridops.app.jenkins_agents_rke2
```

Run it:

```bash
ansible-playbook -i <inventory> deployment/playbooks/configure_jenkins_agents_rke2.yml
```

### 4) Validate agent provisioning

In Jenkins, run a minimal pipeline targeting the label:

```groovy
pipeline {
  agent { label 'rke2-infra' }
  stages {
    stage('proof') {
      steps {
        sh 'whoami && uname -a'
        sh 'kubectl version --client=true'
        sh 'terraform version | head -n 1'
      }
    }
  }
}
```

In RKE2:

```bash
kubectl get pods -n ci-agents -o wide
kubectl describe pod -n ci-agents <pod>
kubectl logs -n ci-agents <pod> --tail 200
```

---

## Validation

Success looks like:

- Controller remains stable and does not run workload on the controller host (executors remain `0` in steady state).
- Agent pods are created in the expected namespace, connect to Jenkins, execute stages, and terminate.
- Jenkins node list shows ephemeral Kubernetes agents rather than persistent controller executors.

<!-- STUB_BREAK: content below may be academy-only when access: academy and stub.enabled=true -->

## Troubleshooting

### Pods are not being created

- Confirm Jenkins can reach the Kubernetes API server from `ctrl-01`.
- Confirm the bearer token is valid and RBAC allows pod creation in the namespace.
- Confirm the cloud name/namespace in JCasC matches your intent.

### Agent pod starts but never connects to Jenkins

- Confirm Jenkins URL / tunnel settings in the Kubernetes cloud definition.
- Confirm network reachability from the cluster to the controller endpoint.

### JCasC boot failure after applying changes

- Check controller logs:

  ```bash
  docker logs --tail 200 jenkins-controller
  ```

- Validate the rendered YAML is valid and uses supported JCasC attributes for your Jenkins/plugin versions.

---

## References

- [ADR-0603 – Run Jenkins controller on control node; agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-jenkins-controller-docker-agents-rke2/)
- [ADR-0202 – Adopt RKE2 as primary runtime](https://docs.hybridops.studio/adr/ADR-0202-rke2-primary-runtime-for-platform-and-apps/)
- [Role: `hybridops.app.jenkins_agents_rke2`](https://github.com/hybridops-studio/ansible-collection-app/tree/main/roles/jenkins_agents_rke2)

---

**Maintainer:** HybridOps.Studio  
**License:** MIT-0 for code; CC BY 4.0 for documentation
