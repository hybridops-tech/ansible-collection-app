# Changelog

All notable changes to the `hybridops.app` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- No unreleased changes yet.

## [0.1.3] - 2026-03-14

### Changed

- Added an explicit Jenkins smoke contract so `hyops test role` can fail early when required runtime secrets are missing.
- Prepared the collection runtime inside CI before direct `ansible-lint` so smoke playbooks resolve `hybridops.app` consistently on GitHub runners.
- Normalized the Jenkins smoke playbook for stricter direct lint execution.

## [0.1.2] - 2026-03-13

### Changed

- Cleaned the published app-role metadata, README surface, and CI release path.
- Normalized the active EVE-NG, NetBox, and Jenkins role YAML so the release branch stays Galaxy-ready.

## [0.1.1] - 2026-03-10

### Changed

- Normalized YAML in the active `pgbackrest_repo` and `netbox_service` task paths for clean Galaxy release linting.
- Updated repository links to the `hybridops-tech` namespace.

## [0.1.0] - 2026-01-02

### Added

- Initial publication of the `hybridops.app` collection.
- Application and platform roles for HybridOps, including initial roles such as:
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

[Unreleased]: https://github.com/hybridops-tech/ansible-collection-app/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/hybridops-tech/ansible-collection-app/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/hybridops-tech/ansible-collection-app/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/hybridops-tech/ansible-collection-app/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/hybridops-tech/ansible-collection-app/releases/tag/v0.1.0
