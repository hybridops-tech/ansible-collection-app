---
title: "Runbook – Jenkins Controller and Agents"
category: "platform"
summary: "Operate and recover the Jenkins CI control plane: controller on ctrl-01 (Docker Compose) with a bootstrap Docker agent and steady-state RKE2 pod agents."
severity: "P2"
topic: "jenkins-controller-agents"
draft: false
is_template_doc: false
tags: ["jenkins", "cicd", "docker", "rke2", "platform"]
access: public
stub:
  enabled: false
  blurb: ""
  highlights: []
  cta_url: ""
  cta_label: ""
---

# Runbook – Jenkins Controller and Agents

**Purpose:** Restore and validate Jenkins controller and agent execution for platform pipelines.  
**Owner:** Platform / SRE  
**Trigger:** Controller health check failing, UI unreachable, job queue backing up, agents offline.  
**Impact:** CI/CD orchestration degraded or unavailable; evidence emission may be incomplete.  
**Severity:** P2 (upgrade to P1 if platform changes are blocked during an active incident window).  
**Pre-reqs:** SSH access to the controller host, Docker Engine + Compose v2, Jenkins admin access, and RKE2 `kubectl` access (when applicable).  
**Rollback strategy:** Roll back to last known-good controller image tag and/or restore `JENKINS_HOME` snapshot/backup; revert JCasC changes from Git.

## HOWTOs

- [HOWTO – Bootstrap Jenkins Controller on Control Node (ctrl-01)](../../howto/platform/HOWTO_bootstrap_jenkins_controller_ctrl01_final.md)
- [HOWTO – Bootstrap Jenkins Docker Agent on Control Node (ctrl-01)](../../howto/platform/HOWTO_bootstrap_jenkins_docker_agent_ctrl01_final.md)
- [HOWTO – Configure Jenkins Agents on RKE2](../../howto/platform/HOWTO_configure_jenkins_agents_rke2_final.md)
- [CI – Jenkins Agents on RKE2 (Pod Templates and Labels)](../../ci/CI-0604-jenkins-agents-rke2.md)

## Scope

This runbook covers:

- Jenkins controller running on `ctrl-01` as a Docker Compose stack.
- Bootstrap execution on a Docker inbound agent (temporary).
- Steady-state execution on agents provisioned as pods in RKE2.

This runbook does not cover:

- Rebuilding `ctrl-01` from scratch (use the controller bootstrap HOWTO and VM restore procedures).
- RKE2 cluster outage recovery (use Kubernetes / DR runbooks).

## Standard and bootstrap exception

- **Standard:** Controller-only mode with **0 executors**. All workload runs on agents.  
- **Bootstrap / lab:** Temporarily set **1 executor** for smoke tests and initial validation, then revert to **0** once agents are online.

## Signals and quick triage

### Symptoms

- Jenkins UI unreachable (connection refused / HTTP 5xx / repeated restart loop).
- Controller container unhealthy or restarting.
- Job queue grows; agents offline; no executors available.
- Kubernetes agents fail to start; pods pending or failing.

### Quick checks (controller host)

```bash
docker version
docker compose version

docker ps --format "table {{.Names}}	{{.Status}}	{{.Image}}"
docker compose -f /opt/jenkins/docker-compose.yml ps

curl -sS -o /dev/null -w "HTTP=%{http_code}
" http://localhost:8080/login || true
```

**Good** looks like:

- `jenkins-controller` is **Up** and (if enabled) **healthy**.
- `/login` returns `200` or `302`.

## Procedure A: Restore controller availability

### A1. Confirm Docker Engine and Compose v2

```bash
docker version
docker compose version
systemctl status docker --no-pager
```

If `docker compose` is missing, apply the Docker baseline and re-check.

### A2. Inspect controller logs (primary signal)

```bash
docker logs jenkins-controller --tail 250
```

Common hard failures:

- **JCasC boot failure** (bad YAML or unsupported attributes)
- **JENKINS_HOME permissions** (cannot write under `/var/jenkins_home`)
- **Plugin resolution / plugin dependency conflicts**

### A3. Fix `JENKINS_HOME` permissions (common)

If logs show write/permission errors under `/var/jenkins_home`:

```bash
sudo ls -ld /opt/jenkins /opt/jenkins/jenkins_home
sudo chown -R 1000:1000 /opt/jenkins/jenkins_home
sudo chmod -R u+rwX,g+rwX /opt/jenkins/jenkins_home
```

Restart stack:

```bash
docker compose -f /opt/jenkins/docker-compose.yml down
docker compose -f /opt/jenkins/docker-compose.yml up -d
```

### A4. Validate JCasC fragments (common)

If Jenkins is failing early with Configuration-as-Code errors:

```bash
sudo ls -la /opt/jenkins/jenkins_home/casc_configs/
sudo sed -n '1,160p' /opt/jenkins/jenkins_home/casc_configs/00-controller.yaml
sudo sed -n '1,220p' /opt/jenkins/jenkins_home/casc_configs/30-nodes-docker.yaml
```

Known issues and fixes:

- **`UnknownAttributesException … DumbSlave : description`**  
  Use `nodeDescription` instead of `description` for permanent nodes.

- **`We only support scalar map keys`**  
  YAML structure is invalid (often caused by templating producing non-scalar map keys). Re-render JCasC with corrected templates and restart.

### A5. Roll back controller image (if failure follows a change)

1. Identify available tags:

```bash
docker images | head -n 30
```

2. Pin compose to the last known-good tag (or re-run the role with a pinned `jenkins_version`) and restart:

```bash
docker compose -f /opt/jenkins/docker-compose.yml up -d
```

## Procedure B: Restore bootstrap Docker agent execution

### B1. Confirm container and connectivity

```bash
docker ps --format "table {{.Names}}	{{.Status}}	{{.Image}}" | egrep "jenkins-controller|jenkins-agent|NAME"
docker logs --tail 120 jenkins-agent-ctrl-docker || true
```

### B2. Confirm the Jenkins node is online (API token)

```bash
TOKEN="$(sudo sh -c 'tr -d "
" </opt/jenkins/.secrets/admin_api_token')"
curl -g -sS -u "admin:${TOKEN}"   "http://localhost:8080/computer/api/json?tree=computer[displayName,offline,offlineCauseReason]"   | head -c 1200 && echo
```

### B3. If the agent is flapping (restarting)

1. Confirm the inbound secret is set (non-empty).
2. Confirm `JENKINS_URL` resolves inside the Docker network:

```bash
docker run --rm --network jenkins --entrypoint /bin/bash   hybridops/ci-agent-tools:0.1.0 -lc 'getent hosts jenkins-controller && curl -sI http://jenkins-controller:8080/login | head -n 5'
```

3. If WebSocket is unreliable in your environment, set `jenkins_agents_docker_use_websocket=false` and re-apply the role.

## Procedure C: Restore RKE2 pod agent execution

### C1. Validate RKE2 agent pods and logs

```bash
kubectl get pods -n <agents-namespace> -o wide
kubectl describe pod -n <agents-namespace> <pod>
kubectl logs -n <agents-namespace> <pod> --tail 200
```

### C2. Validate controller ↔ cluster connectivity

- Controller host can reach the Kubernetes API endpoint.
- RBAC permits pod create/delete in the agents namespace.
- Jenkins cloud config (JCasC) is present under `casc_configs/` and controller has reloaded.

## Verification

Run all applicable checks:

- Controller is stable for 5+ minutes:

```bash
docker ps --format "table {{.Names}}	{{.Status}}	{{.Image}}" | egrep "jenkins-controller|NAME"
curl -sS -o /dev/null -w "HTTP=%{http_code}
" http://localhost:8080/login
```

- Agents are online (bootstrap Docker agent and/or RKE2 agents).
- A minimal pipeline schedules and completes on the target label(s).

## Post-actions and clean-up

- Revert controller executors to **0** once agents are available.
- Capture logs and diagnostics to your evidence store.
- Codify manual fixes back into roles/templates (permissions, JCasC corrections, image pinning).

## References

- ADRs:
  - [ADR-0603 – Run Jenkins Controller on Control Node, Agents on RKE2](../../adr/ADR-0603-jenkins-controller-docker-agents-rke2.md)
  - [ADR-0608 – Docker Engine baseline](../../adr/ADR-0608-docker-engine-baseline.md)
  - [ADR-0202 – Adopt RKE2 as Primary Runtime](../../adr/ADR-0202-rke2-primary-runtime-for-platform-and-apps.md)

- Vendor docs:
  - [Jenkins documentation](https://www.jenkins.io/doc/)
  - [Jenkins Configuration as Code plugin](https://github.com/jenkinsci/configuration-as-code-plugin)
  - [Docker Compose documentation](https://docs.docker.com/compose/)

---

**Maintainer:** HybridOps.Studio  
**License:** See the licensing overview on the documentation site for project-wide licence details, including branding and trademark notes.
