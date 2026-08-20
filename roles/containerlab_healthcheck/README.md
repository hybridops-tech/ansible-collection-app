# hybridops.app.containerlab_healthcheck

Checks the host and deployed lab without taking over Containerlab topology or convergence behaviour.

Checks can cover:

- runtime readiness;
- pinned Containerlab version;
- KVM when the declared workload requires VM-backed nodes;
- declared image references;
- topology validation;
- inspection of an already-deployed lab.

`containerlab_healthcheck_labdir_base` keeps validation and inspection aligned with the same generated lab data used during deployment.

Inspected nodes must report `state=running`. If Containerlab reports health status, the component also rejects `unhealthy` and starting states. Containerlab still performs the topology validation and deployment checks.
