# Changelog

All notable changes to the `jenkins_controller` role are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this role follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-04

### Added

- Initial release of `hybridops.app.jenkins_controller` aligned with ADR-0603
  (run Jenkins controller on control node; run workloads on agents).
- Docker-based Jenkins controller deployment on a Linux control node using
  `docker compose` and a custom image derived from `jenkins/jenkins:lts`.
- Jenkins Configuration as Code (JCasC) via templated `jenkins.yaml.j2`,
  rendered into `JENKINS_HOME`.
- Plugin set management via `plugins.txt`, baked into the controller image at
  build time.
- Host-mounted `JENKINS_HOME` layout under configurable `jenkins_home_path`,
  including UID/GID mapping variables for predictable volume permissions.
- Optional HTTP health check and wait logic for the Jenkins web endpoint.
- Guard tasks that fail fast when Docker Engine or Docker Compose v2 are not
  available on the target host, with guidance to apply the
  `hybridops.common.docker_engine` baseline (ADR-0602).
- Controller executor policy aligned with ADR-0603:
  - `numExecutors: 0` by default (controller-only).
  - Optional `jenkins_controller_num_executors` override for bootstrap / smoke
    validation before agents are configured.
- Smoke test playbook under `roles/jenkins_controller/tests/smoke.yml`.
- Role README documenting purpose, variables, supported platforms, licensing,
  and platform integration context.
