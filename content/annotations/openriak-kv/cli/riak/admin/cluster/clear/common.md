# Metadata

command: shell:riak admin cluster clear
versions: 3.4.0, 3.4.1

# Summary

Discard staged cluster membership changes.

# Description

Clears staged changes that have not been committed. It does not undo completed handoffs or committed membership changes.

# Arguments

# Errors

## reference-error-1

### Condition

The ring has not converged, or the plan changed.

### Description

Planning or committing is refused until the ring is ready and the reviewed plan matches current staging.

### Remedy

Inspect ring-status, wait for convergence, then run cluster plan again.

# Reviewed against

3.4.0: b894b476a522cb3b33889dc99838dd91577bb89d82fc47eab194206904be6a07
3.4.1: b894b476a522cb3b33889dc99838dd91577bb89d82fc47eab194206904be6a07

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
