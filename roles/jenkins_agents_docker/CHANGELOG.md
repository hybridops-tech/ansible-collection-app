# Changelog

All notable changes to the `jenkins_agents_docker` role are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this role follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-08

### Added

- Initial release of `hybridops.app.jenkins_agents_docker` aligned with ADR-0603
  (controller on control node; bootstrap execution on Docker agent; steady-state on RKE2 agents).
- Docker-based Jenkins inbound agent deployment on the controller host using
  `community.docker.docker_container`.
- Controller network handling:
  - Ensures the controller Docker network exists (default: `jenkins`).
  - Attaches the agent container to the controller network for service-name resolution.
- Agent secret handling:
  - Supports supplying `jenkins_agents_docker_agent_secret` directly (no Jenkins API calls).
  - When secret is not supplied, retrieves the inbound secret from
    `/computer/<name>/slave-agent.jnlp` using admin credentials (API token preferred).
  - Clear failure modes when the node is missing (404) or authentication is invalid.
- Optional node management (`jenkins_agents_docker_manage_node`):
  - Can create/ensure the node exists via Jenkins Script Console (`/scriptText`) for bootstrap labs.
  - Designed to be disabled for hardened Jenkins; recommended path is node definition via JCasC.
- Connectivity modes:
  - Supports WebSocket mode via `JENKINS_WEB_SOCKET` (default disabled).
  - Supports legacy JNLP TCP mode (via controller agent port / tunnel settings).
- Docker socket integration:
  - Optional mount of `/var/run/docker.sock` into the agent container for host Docker CLI usage.
  - Discovers host socket GID and passes it as a supplemental group for access.
- Role README documenting purpose, security considerations, variables, usage examples, and validation steps.
