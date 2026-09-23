# Metadata

command: shell:riak admin ensemble-status
versions: 3.4.0, 3.4.1

# Summary

Inspect the strong-consistency ensemble subsystem.

# Description

Without an ensemble selector, show the consensus-system summary. `root` selects the root ensemble. A cluster that has not enabled strong consistency reports the subsystem as disabled.

# Arguments

## ensemble

datatype: ensemble selector
required: false
repeatable: false

### Description

Select a particular ensemble, for example `root`. Omit to show the overall consensus-system summary.

# Reviewed against

3.4.0: 50962fb5fbf9f0c7df785b6817b70e293b61a3344c45541bf7976abd64d740a8
3.4.1: 50962fb5fbf9f0c7df785b6817b70e293b61a3344c45541bf7976abd64d740a8

# Tags

feature: observability
repository: riak_kv
module: riak_kv_console
concept: diagnostics
