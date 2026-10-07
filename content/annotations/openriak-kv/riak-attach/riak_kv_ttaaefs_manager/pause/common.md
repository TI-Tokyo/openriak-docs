# Metadata

command: erlang:riak_kv_ttaaefs_manager:pause/0
versions: 3.4.0, 3.4.1

# Summary

Pause full-sync management on the local node.

# Description

Stops scheduling full-sync work from this manager. This does not itself disable realtime replication.

# Notes

These settings affect the current node. Runtime environment changes are not a replacement for persistent configuration.

# Arguments

# Reviewed against

3.4.0: fcf9d15f90474ec7707c54a6031b50c9032ae32348c31fad94651ab5797c1f6c
3.4.1: 21d16dd2dc20ef774c71a2c7b9e0b927b141b2c8c167fa15aac665456a463e0c

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair
