# Changelog

All notable changes to the `hybridops.app` collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.13] - 2026-09-17

### Added

- Added pinned Containerlab API and web GUI components with loopback-only web
  publication and Linux account authentication.

### Fixed

- Materialised validated same-directory Containerlab saved-configuration links
  as regular files before creating portable recovery archives.
- Prevented Containerlab teardown from inspecting or pulling declared images.
- Avoided refreshing package metadata when the requested Docker package is
  already installed.
- Avoided refreshing package metadata when all Containerlab image-build
  dependencies are already installed.
- Kept staged and restored Containerlab topology trees readable by the declared
  operator account.

## [0.1.12] - 2026-09-16

### Added

- Added checksum-aware loading of operator-supplied Containerlab image
  archives on fresh managed hosts.
- Added managed-host builds for operator-supplied Cisco IOL-XE binaries and
  supported OCI archives using a pinned vrnetlab revision, with structural
  validation before build.
- Added standard CML directory discovery for IOL-XE image type, version,
  checksum, build tag and post-build verification.

### Fixed

- Reset and revalidated SSH after Docker installation on fresh Containerlab
  hosts.
- Preserved and restored the inspected Containerlab native lab directory so
  Cisco IOL NVRAM survives disposable-host reconstruction.

## [0.1.11] - 2026-09-15

### Fixed

- Prevented additional EVE-NG user credentials from appearing in task output.

## [0.1.10] - 2026-08-26

### Added

- Added a fail-closed GNS3 restore capacity check before existing project and
  node-state data is replaced.

### Fixed

- Bound the EVE-NG Guacamole daemon and web application to the same IPv4
  loopback endpoint and verified both services before configuration completes.
- Staged and verified GNS3 project exports before promotion, retaining one
  verified fallback archive and manifest.

## [0.1.9] - 2026-08-22

### Added

- Added opt-in private management bridges with DHCP lease evidence for EVE-NG
  and GNS3 device automation access, including a subnet-scoped OpenSSH tunnel
  for direct Linux and WSL routing.
- Added GNS3 QEMU and IOU image acquisition from HTTP, HTTPS and MEGA sources,
  including safe archive extraction, automatic payload mapping, optional
  checksums, and template registration.
- Added protected operator-supplied IOU licence handling, hostname binding
  validation, and support for older 32-bit images.
- Added a pinned Containerlab runtime, native lab operations, independent
  health checks, and guarded off-host recovery for disposable hosts.

### Fixed

- Preserved Core-selected Containerlab export, import, and destroy actions when
  deploy-time inputs remain present during rebuild and teardown.
- Isolated GNS3 management DHCP from libvirt's dnsmasq configuration so a new
  server can start both services without conflicting bind modes.

## [0.1.8] - 2026-07-19

### Added

- Added checksum-verified export and restore for GNS3 projects, controller
  metadata, and writable node disks.

### Fixed

- Removed stale GNS3 repository metadata before package refresh.
- Aligned the Ubuntu 24.04 GNS3 server package with the current repository
  release.

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
