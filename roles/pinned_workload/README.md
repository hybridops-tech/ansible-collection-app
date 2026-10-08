# pinned_workload

Materialises an external Git repository at an exact commit, executes one
declared entry point and retains the declared result paths on the controller.

The workload remains responsible for its own operation and acceptance logic.
This role records the execution binding and retained evidence needed by the
surrounding host lifecycle.

Required inputs:

- `pinned_workload_id`
- `pinned_workload_repository`
- `pinned_workload_revision`, as a full 40-character commit SHA
- `pinned_workload_entrypoint`, relative to the repository root
- `pinned_workload_evidence_paths`, relative to the repository root
- `pinned_workload_controller_evidence_dir`

`pinned_workload_runtime_files` accepts controller-side files that must be
staged before execution. Each item declares `src`, `dest` and an optional
`mode`. Contents are not logged.
