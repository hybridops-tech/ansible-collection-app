# Changelog

All notable changes to the `hybridops.app` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- No unreleased changes yet.

## [0.1.0] - 2026-01-02

### Added

- Initial publication of the `hybridops.app` collection.
- Application and platform roles for HybridOps.Studio, including initial roles such as:
  - `control_node_secrets_guard`
  - `jenkins_controller`
  - `linux_deploy_nginx`
  - `linux_rke2_install`
  - `moodle_stack`
  - `netbox_bootstrap`
  - `netbox_seed`
  - `rke2_controlplane`
  - `windows_configure_cluster`
  - `windows_domain_join`
  - `windows_install_sql`
  - `windows_windows_updates`
- Role-local `tests/` harnesses and optional Molecule scenarios for selected roles.
- `galaxy.yml` metadata for namespace `hybridops` and collection name `app`.

[Unreleased]: https://github.com/hybridops-studio/ansible-collection-app/compare/v0.1.0-app...HEAD
[0.1.0]: https://github.com/hybridops-studio/ansible-collection-app/releases/tag/v0.1.0-app
