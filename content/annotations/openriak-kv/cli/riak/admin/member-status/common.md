# Metadata

command: shell:riak admin member-status

# Summary

Inspect cluster membership and current and pending ring ownership.

# Description

Inspect the membership view reported by this node. Check node states, current ring ownership and pending ownership before changing cluster membership.

# Notes

A successful membership query does not establish that every client operation or replication relationship is healthy.

# Examples

## member-status:healthy-node

### Description

Inspect a healthy, one-node example cluster. It owns 100% of the ring. A multi-node cluster will show additional rows and different ownership percentages.

# Reviewed against

3.4.0: 0f5d6b41611f17fb438038c28e98d43a81ec6b01c71844b8cc67bab05475c2e4
3.4.1: 0f5d6b41611f17fb438038c28e98d43a81ec6b01c71844b8cc67bab05475c2e4

# Tags

feature: observability
repository: riak_core
module: riak_core_console
concept: diagnostics
