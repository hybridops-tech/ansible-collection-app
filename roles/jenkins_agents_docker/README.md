# Role: jenkins_agents_docker

Configures a **bootstrap Jenkins inbound agent** that runs as a Docker container on the controller host (for example `ctrl-01`).

This role supports the **bootstrap / transition phase** where the Jenkins controller is already deployed (via `jenkins_controller`), but the primary execution runtime (RKE2 pod agents) is not yet available. In steady state, agents are expected to run on RKE2 using `jenkins_agents_rke2`, aligned with the execution model in [ADR-0603 – Run Jenkins controller on control node, agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-jenkins-controller-docker-agents-rke2/).

---

## When to use

Use this role when you need:

- A **repeatable bootstrap agent** to run early pipelines (image builds, infra provisioning, configuration management) before RKE2 exists.
- A **controlled fallback** execution surface on the controller host (for example, when RKE2 agents are temporarily unavailable).

Do not use this role as the long-term execution model. For steady-state operation, prefer RKE2 pod agents.

---

## What this role does

- Validates Jenkins controller reachability on the host-local API endpoint.
- Ensures the controller Docker network exists (default: `jenkins`).
- Ensures an inbound agent container is running on the controller Docker network.
- Retrieves the agent’s inbound secret from `slave-agent.jnlp` when not supplied and Jenkins API access is provided.
- Optionally creates/ensures a Jenkins node via the Script Console endpoint (`/scriptText`) when explicitly enabled.

---

## Requirements

Target host requirements:

- Docker Engine installed and running.
- Jenkins controller already deployed and reachable on the host (typically `http://localhost:8080`).
- Network reachability from the agent container to the controller service name on the Docker network (default: `jenkins-controller:8080`).

Jenkins requirements (only when `jenkins_agents_docker_manage_node=true`):

- Admin credentials (password or API token) with permission to access:
  - `GET /crumbIssuer/api/json` (when CSRF is enabled)
  - `POST /scriptText` (Script Console)
  - `GET /computer/<node>/slave-agent.jnlp`

If your Jenkins is hardened with Script Console disabled, set `jenkins_agents_docker_manage_node=false` and provision the node via JCasC (recommended) or provide `jenkins_agents_docker_agent_secret` out of band.

---

## Security considerations

- **Docker socket mounting** (`/var/run/docker.sock`) grants the container root-equivalent control of the host Docker daemon. Enable only on controlled hosts and only when required for bootstrap workflows.
- **Script Console usage** (`/scriptText`) is powerful. In hardened environments, disable automated node creation and manage nodes via approved Jenkins configuration flows (prefer JCasC).
- Avoid printing secrets to logs. This role treats credentials and secrets as sensitive and uses `no_log` for API calls.

---

## Role variables

Defaults are defined in `defaults/main.yml`. Key variables:

| Variable | Default | Purpose |
|---|---|---|
| `jenkins_agents_docker_enabled` | `true` | Enable/disable the role per host. |
| `jenkins_agents_docker_api_url` | `http://localhost:8080` | Host-local Jenkins API endpoint used by Ansible. |
| `jenkins_agents_docker_jenkins_url` | `http://jenkins-controller:8080` | Controller URL reachable **from the Docker network**. |
| `jenkins_agents_docker_jenkins_tunnel` | `jenkins-controller:50000` | TCP agent listener target (used when WebSocket is not used). |
| `jenkins_admin_username` | `admin` | Jenkins admin username used for API calls. |
| `jenkins_admin_password` | `""` | Admin password (bootstrap). Prefer Vault/group_vars. |
| `jenkins_admin_api_token` | `""` | Optional API token used as the Basic Auth “password”. |
| `jenkins_agents_docker_manage_node` | `true` | When `true`, attempts to create/ensure the node via Script Console if the secret is not provided. |
| `jenkins_agents_docker_script_text_url` | `{{ jenkins_agents_docker_api_url }}/scriptText` | Script Console endpoint for node creation. |
| `jenkins_agents_docker_label` | `ctrl-docker` | Label assigned to the Jenkins node. |
| `jenkins_agents_docker_agent_name` | `ctrl-docker` | Node name and agent name. |
| `jenkins_agents_docker_container_name` | `jenkins-agent-ctrl-docker` | Docker container name for the agent. |
| `jenkins_agents_docker_agent_image` | `hybridops/ci-agent-tools:0.1.0` | Agent image (tools-enabled inbound agent). |
| `jenkins_agents_docker_use_websocket` | `false` | Use WebSocket transport for inbound agent connections. |
| `jenkins_agents_docker_agent_secret` | `""` | If set, skips Jenkins API calls and uses this secret directly. |
| `jenkins_agents_docker_mount_docker_socket` | `true` | Mount host Docker socket into the agent container. |
| `jenkins_agents_docker_docker_socket_path` | `/var/run/docker.sock` | Socket path to mount. |

---

## Usage

### Managed bootstrap (node created or ensured via Script Console)

Use this for labs and controlled environments where Script Console access is allowed.

```yaml
- name: Configure Jenkins bootstrap docker agent on ctrl-01
  hosts: ctrl_nodes
  become: true

  collections:
    - hybridops.app

  vars:
    jenkins_agents_docker_api_url: "http://localhost:8080"
    jenkins_agents_docker_jenkins_url: "http://jenkins-controller:8080"

    jenkins_admin_username: "admin"
    jenkins_admin_api_token: "{{ vault_jenkins_admin_api_token }}"

    jenkins_agents_docker_manage_node: true
    jenkins_agents_docker_use_websocket: false

  roles:
    - role: jenkins_agents_docker
```

### Hardened Jenkins (no Script Console) + secret managed out of band

Recommended for public / locked-down Jenkins environments.

```yaml
- name: Configure Jenkins bootstrap docker agent (hardened)
  hosts: ctrl_nodes
  become: true

  collections:
    - hybridops.app

  vars:
    jenkins_agents_docker_manage_node: false
    jenkins_agents_docker_agent_secret: "{{ vault_ctrl_docker_agent_secret }}"
    jenkins_agents_docker_use_websocket: false

  roles:
    - role: jenkins_agents_docker
```

---

## Validation

After the role runs:

- The agent container is running:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
```

- Jenkins shows the node online (example, using an API token):

```bash
TOKEN="$(sudo sh -c 'tr -d "\n" </opt/jenkins/.secrets/admin_api_token')"
curl -g -sS -u "admin:${TOKEN}"   "http://localhost:8080/computer/api/json?tree=computer[displayName,offline]"   | head -c 600 && echo
```

- A pipeline can target the label:

```groovy
pipeline {
  agent { label 'ctrl-docker' }
  stages {
    stage('proof') {
      steps {
        sh 'whoami && uname -a && terraform version | head -n 1'
      }
    }
  }
}
```

---

## Troubleshooting

- **Agent container restarts**  
  Check container logs and confirm `JENKINS_URL`, `JENKINS_AGENT_NAME`, and `JENKINS_SECRET` are set correctly.

  ```bash
  docker logs --tail 80 jenkins-agent-ctrl-docker
  ```

- **Jenkins auth succeeds for `/whoAmI` but node management fails**  
  Script Console may be disabled or requires additional permissions. Prefer JCasC node definition and set `jenkins_agents_docker_manage_node=false`.

- **JNLP endpoint returns 404**  
  The node does not exist. Create the node via controller JCasC (recommended) or provide `jenkins_agents_docker_agent_secret`.

- **Docker CLI not usable in the agent**  
  Ensure `jenkins_agents_docker_mount_docker_socket=true`, the host socket exists, and the role adds the socket GID as a supplemental group.

---

## Related references

- [ADR-0603 – Run Jenkins controller on control node, agents on RKE2](https://docs.hybridops.studio/adr/ADR-0603-jenkins-controller-docker-agents-rke2/)  
- [ADR-0607 – Adopt CI agent tools image for Jenkins agents](https://docs.hybridops.studio/adr/ADR-0607-adopt-ci-agent-tools-image-for-jenkins-agents/)  
- [Runbooks](https://docs.hybridops.studio/ops/runbooks/)  

---

**Maintainer:** HybridOps.Studio  
**License:** See the [HybridOps.Studio licensing overview](https://docs.hybridops.studio/briefings/legal/licensing/) for project-wide licence details.
