# GNS3 images

Acquire QEMU or IOU images and register matching GNS3 templates.
Existing matching templates are retained. A name conflict with another image
fails without replacing the existing template.

The compact declaration matches the EVE-NG image workflow. `name` identifies
the downloaded file, `label` names the GNS3 template, and `type: iol` is
accepted as an alias for GNS3 `iou`:

```yaml
gns3_images_items:
  - url: https://example.invalid/iol-router.tar.gz
    name: iol-router.tar.gz
    type: iol
    label: Authorised IOU router
```

HTTP, HTTPS and MEGA links are supported. Raw images and archives are accepted.
An archive must contain exactly one primary payload: `.bin` for IOU or `.qcow2`,
`.img` or `.iso` for QEMU. A QEMU archive may also contain one disk with
`DATASTOR` in its filename; it is registered as the template's second disk.
The role maps each payload to the GNS3 image directory and registers the
template. `checksum` is optional; when supplied it must use
`sha256:<64-hex-characters>` and applies to the downloaded source artifact.

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

The role installs IOU runtime support only when an IOU or IOL item is declared.
The licence must contain an entry for the current GNS3 hostname.
The role reports that hostname when the binding does not match. The licence is
written with mode `0600`, is never logged, and is not included in project
archives. Image and licence acquisition remain the operator's responsibility;
the role does not generate licences, bundle appliances, or bypass vendor
controls. QEMU guest activation remains a guest-level concern.
