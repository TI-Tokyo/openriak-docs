# Description

Throttles legacy anti-entropy tree construction with a `{ByteLimit, DelayMilliseconds}` pair. Once the fold has processed more than the byte limit, it sleeps for the delay; a zero byte limit disables the pause.

# Datatype

Tuple

# Constraints

- `{ByteLimit, WaitMilliseconds}` with non-negative integers. `ByteLimit = 0` disables throttling; otherwise the build sleeps after exceeding the byte budget.

# Inferred default

`{1000000, 100}`.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_index_hashtree
concept: replica-repair, scheduling

# Notes

This is the Erlang application environment key `anti_entropy_build_throttle` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_index_hashtree.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_index_hashtree.erl#L650)

# Reviewed against

3.4.0: 5c74130feb6cadd1d4c481d509e73ffd2136080f57191725b43437b369fe2cff
3.4.1: a2d59ff7426466e66137471ee1d604d9eb191c896e7aa7390d5dd9bb8cf773cd
