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

3.4.0: 1f98971323e8a9efca0090b427918b32bc6acf5bf20ce577f3728ccf2b38ca99
3.4.1: b531e81c5b23ffa230cb6d62514eae73d882023396ce5f2a4548ddadfb65ff7d

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
