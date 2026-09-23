# Metadata

command: shell:riak admin cluster resize-ring abort
versions: 3.4.0, 3.4.1

# Summary

Stage cancellation of an in-progress ring resize.

# Description

Cancellation is a staged operation and is unavailable after resizing completes.

# Arguments

# Results

## reference-result-1

### Description

When a resize can be cancelled, prints a staged abort confirmation. Review and commit the resulting plan.

# Reviewed against

3.4.0: 87cb0fa7a11222a762337a7d15a9ef3d51441051418cbd7682cf134c8ad94a5d
3.4.1: 87cb0fa7a11222a762337a7d15a9ef3d51441051418cbd7682cf134c8ad94a5d

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
