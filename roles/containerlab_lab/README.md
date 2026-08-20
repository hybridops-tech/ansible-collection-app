# hybridops.app.containerlab_lab

Runs lab operations through Containerlab while keeping the supplied topology authoritative.

Supported actions:

- `validate`
- `deploy` including supported restore handoff
- `inspect`
- `destroy`
- `redeploy`
- native configuration save
- supported snapshot save

`containerlab_lab_labdir_base` keeps generated `clab-*` data outside the staged source tree.

`containerlab_lab_required_images` is an optional preflight list. Missing images are fetched only when `containerlab_lab_pull_missing_images` is enabled. This component does not distribute proprietary NOS images.
