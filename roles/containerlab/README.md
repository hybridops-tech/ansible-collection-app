# hybridops.app.containerlab

Prepares a pinned Containerlab runtime on Ubuntu and checks KVM when the caller requires VM-backed or vrnetlab workloads.

This component does not define topologies, manage nodes or links, handle convergence, decide image entitlement, or implement lab recovery. Those remain Containerlab responsibilities.

## Key variables

- `containerlab_version` (default `0.78.0`)
- `containerlab_install_docker` (default `true`)
- `containerlab_enable_ipv4_forwarding` (default `true`)
- `containerlab_operator_user`
- `containerlab_require_kvm` (default `false`)
- `containerlab_package_checksum` (optional explicit checksum expression)
- `containerlab_package_checksum_url` (defaults to the pinned release's official `checksums.txt` asset)

Package installation fails closed. An explicit SHA-256 digest is used when supplied. If a known digest exists in `containerlab_package_checksums`, that is used instead. Otherwise the package is verified against the pinned release checksum file.

After download, the package SHA-256 is published in `containerlab_runtime_result` so HybridOps records the exact artifact used.

The package is downloaded from the upstream release for the pinned version and host architecture.

IPv4 forwarding is enabled and persisted for Containerlab and Docker bridge networking. Set `containerlab_enable_ipv4_forwarding` to `false` only when the host network policy manages forwarding separately.
