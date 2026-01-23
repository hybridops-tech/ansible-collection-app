# Changelog

All notable changes to the `jenkins_agents_rke2` role are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this role follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-05

### Added

- Initial release of `hybridops.app.jenkins_agents_rke2`.
- JCasC fragment rendering to configure an RKE2-backed Kubernetes cloud.
- Default pod template and label for Kubernetes agents.
- Bearer-token credential wiring for Jenkins ↔ Kubernetes API access.
- Optional controller restart and readiness wait to apply configuration safely.
