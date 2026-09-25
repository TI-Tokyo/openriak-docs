# Description

In-memory queue limit for the background tombstone reaper. Additional reap references spill into the separately bounded overflow queue while the reaper removes tombstones from replicas.

# Datatype

Integer

# Units

- references

# Constraints

- Expected to be a positive integer.

# Inferred default

`100000`.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_reaper
concept: queueing, tombstones

# Notes

This is the Erlang application environment key `reaper_queue_limit` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_reaper.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_reaper.erl#L162)

# Reviewed against

3.4.0: 4c0ab8477308957c07d7eb1c9089d1f942de5d9dc79d7c604b7312957b52bbb8
3.4.1: ece5b29ea2be9b93d2b694d5200df30fe0b3e7bd17553777aed4312fe935ec18
