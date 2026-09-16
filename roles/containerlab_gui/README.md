# Containerlab GUI

Runs the official Containerlab API server and web GUI on the Linux host that
owns the container runtime and lab files. The web endpoint is published only on
host loopback. The API endpoint is bound to the Docker bridge for access by the
web container.

The login user must already exist on the host. The role grants that user API
access. Password management is opt-in.

```yaml
containerlab_gui_operator_user: opsadmin
containerlab_gui_labs_dir: /var/lib/hybridops/containerlab/labs
containerlab_gui_manage_operator_password: false
```
