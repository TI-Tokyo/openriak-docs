# Description

Pause, in milliseconds, used by the background reaper when cycling retry work. It spaces out attempts to finish reaping tombstones from replicas that were previously unavailable.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a positive integer.

# Inferred default

`2000`.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_reaper
concept: scheduling, tombstones

# Notes

This is the Erlang application environment key `reaper_redo_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_reaper.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_reaper.erl#L160)

# Reviewed against

3.4.0: 6b52fd95c290b41d67ea30a1390b343cf844b90e66343ad789ba9da3049b7eba
3.4.1: d15eae2e6c34df812eeb089d480854cfdded03a6c6e6b6f78bd70bc26ecfb695
