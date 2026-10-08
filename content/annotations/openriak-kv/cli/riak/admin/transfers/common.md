# Metadata

command: shell:riak admin transfers
versions: 3.4.0, 3.4.1

# Summary

Inspect pending and active partition handoffs.

# Description

Run transfers after a cluster commit to follow partition movement. Waiting counts describe work still queued; Active Transfers shows individual handoffs, including partition IDs, source and destination nodes, transferred objects and progress. Run it again to follow changes over time.

# Arguments

# Notes

The examples expand a single-node cluster to five nodes. Node1 holds the original partitions, so it is the source and nodes2 through node5 are receivers. All five nodes participate in the transfer; every node need not be both a sender and a receiver.

Joining nodes can report waiting secondary partitions before commit, while Active Transfers remains empty. A zero transfer limit can leave handoffs waiting after a successful commit. When work finishes, expect no waiting handoffs and an empty Active Transfers section. Check member-status and ring-status as well: an idle transfer display alone does not prove cluster health. Object counts, rates and partition IDs vary with the ring and stored data. A total-size estimate of zero or an `N/A` percentage can accompany positive transferred-object counts; do not read those unavailable estimates as proof that the transfer is empty.

# Related documentation

- [Review the cluster plan](../cluster/plan/)
- [Commit the reviewed plan](../cluster/commit/)
- [Inspect transfer limits](../transfer-limit/)
- [Inspect member status](../member-status/)
- [Inspect ring convergence](../ring-status/)

# Reviewed against

3.4.0: b6b266fe65efdb50a4b684748b415f1203ed6aae1aa306a095e1ba3b77145f36
3.4.1: b6b266fe65efdb50a4b684748b415f1203ed6aae1aa306a095e1ba3b77145f36

# Tags

feature: handoff
repository: riak_core
module: riak_core_console
concept: partition-transfer
