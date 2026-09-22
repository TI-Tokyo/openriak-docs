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

3.4.0: e4614a2aea7d0247e41afee3f43a511baf72b767a8ef0b42ba94ae69990b361b
3.4.1: e4614a2aea7d0247e41afee3f43a511baf72b767a8ef0b42ba94ae69990b361b
