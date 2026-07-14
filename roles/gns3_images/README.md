# GNS3 images

Install checksum-verified QEMU images and register matching GNS3 templates.
Existing matching templates are retained. A name conflict with another image
fails without replacing the existing template.

```yaml
gns3_images_items:
  - name: Alpine Linux
    url: https://example.invalid/alpine.qcow2
    filename: alpine.qcow2
    checksum: sha256:REPLACE_WITH_64_HEX_CHARACTERS
    disk_type: hda
    template:
      ram: 512
      adapters: 2
```

Image licensing remains the operator's responsibility. The role does not
bundle appliance images or bypass vendor download controls.
