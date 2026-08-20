# GNS3 images

Install checksum-verified QEMU or IOU images and register matching GNS3 templates.
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

An authorised IOU image requires a separate, operator-supplied licence:

```yaml
gns3_images_iourc_content: "{{ lookup('env', 'GNS3_IOU_LICENSE') }}"
gns3_images_items:
  - name: Authorised IOU router
    type: iou
    url: https://operator-controlled.example/router.bin
    filename: router.bin
    checksum: sha256:REPLACE_WITH_64_HEX_CHARACTERS
    architecture: i386
    template:
      ethernet_adapters: 4
      serial_adapters: 0
```

The role installs IOU runtime support only when an IOU item is declared. Older
filenames beginning with `i86bi` automatically enable the required `i386`
package architecture; `architecture: i386` can state that requirement
explicitly. The licence is written with mode `0600`, is never logged, and is not included in
project archives. Image and licence acquisition remain the operator's
responsibility; the role does not generate licences, bundle appliances, or
bypass vendor controls. QEMU guest activation remains a guest-level concern.
