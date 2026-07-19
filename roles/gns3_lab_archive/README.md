# gns3_lab_archive

Export GNS3 projects and controller metadata to a verified controller-side
archive, then restore them after the server is rebuilt.

Project directories contain the topology, project files and writable node
disks. Base images are excluded by default because the declared image module
can download them again. Set `gns3_lab_archive_include_images: true` only when
the archive must also carry the base-image library.

```yaml
gns3_lab_archive_action: export
gns3_lab_archive_path: /srv/hybridops/gns3/labs.tar.gz
```

Restore requires the recorded SHA-256 checksum:

```yaml
gns3_lab_archive_action: restore
gns3_lab_archive_path: /srv/hybridops/gns3/labs.tar.gz
gns3_lab_archive_expected_sha256: CHANGE_ME
gns3_lab_archive_overwrite: true
```

The server is stopped while controller state is copied or restored and is
started again before the role returns.
