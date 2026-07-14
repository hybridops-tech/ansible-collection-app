# GNS3 health check

Validate an installed GNS3 server without changing its persistent projects or
images. The default check covers the service, API authentication, local compute,
nested KVM, emulator commands and data directories.

Set `gns3_healthcheck_deep: true` to add a disposable VPCS lifecycle. The role
removes the temporary project whether the check succeeds or fails.

```yaml
- name: Check GNS3
  ansible.builtin.include_role:
    name: hybridops.app.gns3_healthcheck
  vars:
    gns3_healthcheck_password: "{{ vault_gns3_password }}"
    gns3_healthcheck_deep: true
```
