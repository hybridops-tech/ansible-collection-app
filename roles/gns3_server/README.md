# GNS3 server

Installs and configures an authenticated GNS3 2.2 server on a dedicated Ubuntu
22.04 or 24.04 x86_64 host. The role manages the stable GNS3 package source,
emulator dependencies, server configuration and systemd service.

The server password is required and should be supplied from a vault or process
environment. The role does not install the desktop client or proprietary
network images.

The collection pins the GNS3 server package independently for each supported
Ubuntu release. Version changes are made through a collection release rather
than an unattended package upgrade.

## Required variable

```yaml
gns3_server_password: "{{ lookup('env', 'GNS3_SERVER_PASSWORD') }}"
```

## Common variables

```yaml
gns3_server_bind_address: "0.0.0.0"
gns3_server_port: 3080
gns3_server_username: "gns3"
gns3_server_install_emulators: true
gns3_server_require_kvm: false
```

The server configuration retains GNS3's licence check and points IOU nodes to
`/var/lib/gns3/.iourc`. The `gns3_images` role creates that file only when an
operator declares an IOU image and supplies authorised licence material.

Enable a private host-reachable management bridge when lab devices must be
automated from the operator workstation:

```yaml
gns3_server_management_access_enabled: true
gns3_server_management_bridge: hyops-mgmt0
gns3_server_management_cidr: 172.29.130.1/24
gns3_server_management_subnet: 172.29.130.0/24
gns3_server_management_dhcp_start: 172.29.130.50
gns3_server_management_dhcp_end: 172.29.130.200
gns3_server_management_access_ssh_user: opsadmin
```

Map a GNS3 Cloud node to `hyops-mgmt0` and connect device management
interfaces to that cloud. The server keeps the subnet private while allowing
the declared access host to reach its devices. Static devices must route
through the address declared by `gns3_server_management_cidr`.
