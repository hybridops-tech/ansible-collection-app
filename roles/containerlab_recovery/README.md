# hybridops.app.containerlab_recovery

Exports and imports recovery data for a Containerlab host that may later be deleted and rebuilt.

## Export

`containerlab_recovery_mode` controls what is retained:

- `ephemeral`: topology, version and inspection metadata;
- `rebuild`: the above plus supported native configuration save output;
- `snapshot`: the rebuild set plus supported vrnetlab snapshots.

`containerlab_recovery_labdir_base` must match the generated lab-data location used when the lab was deployed. Inspect, save and snapshot operations use that same path.

The recovery set is archived and copied to the HybridOps controller. The
retained archive is fully read, checked for unsafe members and matched against
the host-side checksum. `containerlab_recovery_result.safe_for_host_destroy` is
set only after those checks pass.

Generated lab data is not copied by default. Set
`containerlab_recovery_include_lab_dir` to retain it. The role resolves the
active lab directory from native inspection metadata;
`containerlab_recovery_lab_dir` remains available as an explicit source
override. Additional paths can also be listed.

## Import

Import verifies the checksum, member safety, manifest contract and topology
identity before publishing the restored topology path and snapshot directory.

The final restore remains a Containerlab operation. HybridOps passes the restored topology and, when present, supported snapshot data back to Containerlab for deployment.

This component does not distribute vendor images, licences or secrets, and recovery depends on what the relevant Containerlab node kind supports.
