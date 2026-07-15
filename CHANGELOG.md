# Changelog

All notable changes to the `hybridops.app` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- No unreleased changes yet.

## [0.1.7] - 2026-07-15

### Added

- Added optional DHCP, DNS, forwarding, and NAT egress for EVE-NG lab nodes
  through a dedicated private bridge.
- Added persistent service configuration and readiness checks for the guest
  bridge and scoped masquerade rule.
- Added an authenticated GNS3 server role for dedicated Ubuntu hosts.
- Added authenticated GNS3 server health checks with an optional disposable
  VPCS lifecycle.
- Added an idempotent GNS3 starter topology using built-in NAT, Ethernet
  switch and VPCS nodes.
- Added checksum-verified GNS3 QEMU image installation and template
  registration.

### Changed

- Allowed the GNS3 service to create NAT TAP interfaces using scoped network
  capabilities.
- Require `hybridops.helper` 0.1.6 or later so the guest-egress release is
  installed with the corrected EVE-NG image lifecycle.

## [0.1.6] - 2026-06-14

### Changed

- Cleaned public Galaxy metadata so collection references point to the published Galaxy and documentation surfaces.
- Tightened the package surface to exclude local Ansible workspace content, old build archives, and showcase-only assets.

## [0.1.5] - 2026-04-03

### Fixed

- Wired the EVE-NG `Restart sshd` handler to the `restart sshd` listen target so fresh-host installs can complete cleanly.

## [0.1.4] - 2026-03-20

### Changed

- Imported the latest active role content from the core workspace.
- Updated the collection branding to `HybridOps.Tech`.

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
