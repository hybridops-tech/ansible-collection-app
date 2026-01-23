---
title: "CI – Jenkins Agents on RKE2 (Pod Templates and Labels)"
category: "ci"
summary: >
  Define and validate Jenkins agent execution on RKE2: pod templates, labels,
  and baseline connectivity between the controller on ctrl-01 and the cluster.
severity: "P3"
topic: "ci-jenkins-agents-rke2"
draft: false
is_template_doc: false
tags: ["ci", "jenkins", "rke2", "kubernetes"]
access: public
stub:
  enabled: false
  blurb: ""
  highlights: []
  cta_url: ""
  cta_label: ""
---

# CI – Jenkins Agents on RKE2 (Pod Templates and Labels)

## Purpose

Standardise how pipelines select execution environments once the Jenkins controller is online:

- Controller remains the orchestration surface (controller-only).
- Pipeline steps run on labelled agents provisioned as pods in RKE2.

## Scope

Includes:

- Pod template labels and intent.
- Minimum connectivity and validation checks.
- Evidence capture expectations for agent runs.

Excludes:

- Jenkins controller deployment (see the controller HOWTO/runbook).
- RKE2 cluster build, upgrade, or recovery.

## Labels

Baseline labels (extend per workload):

- `rke2-infra` — infrastructure automation steps.
- `rke2-app` — application delivery steps.
- `rke2-docs` — documentation pipelines.

Guidance:

- Each label must map to a **single** pod template with a clear purpose.
- Templates must use a version-pinned agent image (avoid `latest` in production-like paths).

## Validation gates

A label is **not** eligible for general pipeline use until all gates pass.

### Gate 1 — Controller → RKE2 API reachability

From `ctrl-01`:

- Kubernetes API endpoint is reachable (TCP 6443).
- TLS trust is configured (CA or kubeconfig) for the Jenkins Kubernetes cloud.

### Gate 2 — RKE2 → Jenkins agent endpoint reachability

At least one agent pod must be able to connect back to the controller:

- JNLP agent listener reachable (TCP 50000) **or** WebSocket mode is enabled for Kubernetes agents.

### Gate 3 — RBAC for pod lifecycle

Service account used by Jenkins must be able to:

- Create/delete pods in the agents namespace.
- Read pod logs (for evidence and troubleshooting).

### Gate 4 — Proof pipeline on the label

Run a minimal pipeline that:

- Schedules on the label.
- Prints node/pod identity.
- Executes a trivial command and exits successfully.

Example Jenkinsfile:

```groovy
pipeline {
  agent { label 'rke2-infra' }
  stages {
    stage('proof') {
      steps {
        sh 'id && uname -a'
      }
    }
  }
}
```

## Evidence capture

Capture minimum proof for one successful run per label:

### Kubernetes evidence

```bash
kubectl -n <agents_namespace> get pods -o wide
kubectl -n <agents_namespace> describe pod <pod>
kubectl -n <agents_namespace> logs <pod> --tail 200
```

### Jenkins evidence

- Job console output showing:
  - Label requested.
  - Node/pod name used.
- JCasC fragment snapshot used to define the cloud and templates (from the controller JCasC directory).

## References

- HOWTO: [Configure Jenkins Agents on RKE2](https://docs.hybridops.studio/howtos/platform/jenkins-agents-rke2/)
- ADR: [ADR-0603 – Run Jenkins controller on control node; agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-run-jenkins-controller-on-control-node-agents-on-rke2/)
- ADR: [ADR-0202 – Adopt RKE2 as primary runtime](https://docs.hybridops.studio/adr/ADR-0202-adopt-rke2-as-primary-runtime/)
- Runbooks: [Operations runbooks index](https://docs.hybridops.studio/ops/runbooks/)
