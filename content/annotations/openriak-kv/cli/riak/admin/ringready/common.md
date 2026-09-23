# Metadata

command: shell:riak admin ringready
versions: 3.4.0, 3.4.1

# Summary

Check whether cluster members agree on the ring.

# Description

A `TRUE` result lists agreeing nodes. Investigate unreachable or disagreeing members before proceeding with a planned cluster change.

# Arguments

# Reviewed against

3.4.0: 6da64521cf5d768c1bb88d1136f8757a7723d550eda611bd5c071c8238a662c6
3.4.1: 6da64521cf5d768c1bb88d1136f8757a7723d550eda611bd5c071c8238a662c6

# Tags

feature: cluster-management
repository: riak_kv
module: riak_kv_console
concept: partition-placement
