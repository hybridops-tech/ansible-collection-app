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

`containerlab_lab_local_image_archives` loads operator-supplied container image archives
when the expected image is absent. Each entry declares an absolute controller
path, the image reference expected after loading, and an optional SHA-256
digest. The operator remains responsible for image and licence rights.
