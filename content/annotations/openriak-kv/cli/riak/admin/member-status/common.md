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

3.4.0: 08db67ae1eb22e141241e5e8ca9896094480e04b61ddd9e9e87b004794249e8c
3.4.1: 08db67ae1eb22e141241e5e8ca9896094480e04b61ddd9e9e87b004794249e8c
