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

3.4.0: 531c48fca7a0a6fa9d6d8e9c42706ef00aefbc789cba26dab682863c8438e50e
3.4.1: 531c48fca7a0a6fa9d6d8e9c42706ef00aefbc789cba26dab682863c8438e50e
