# Metadata

command: shell:riak admin ringready
versions: 3.4.0, 3.4.1

# Summary

Check whether cluster members agree on the ring.

# Description

A `TRUE` result lists agreeing nodes. Investigate unreachable or disagreeing members before proceeding with a planned cluster change.

# Arguments

# Reviewed against

3.4.0: 3f4f727f37663097f04c9d8d25df881da9148cfc5ace681f49995d23a631abb4
3.4.1: 3f4f727f37663097f04c9d8d25df881da9148cfc5ace681f49995d23a631abb4

# Tags

feature: cluster-management
repository: riak_kv
module: riak_kv_console
concept: partition-placement
