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
