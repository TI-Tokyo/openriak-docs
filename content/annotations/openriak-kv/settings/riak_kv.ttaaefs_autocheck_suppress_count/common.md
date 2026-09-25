# Description

Number of automatic Tictac full-sync checks to suppress when the manager requests a suppression period. The count is copied into the mutable `riak_kv.ttaaefs_autocheck_dropnext` counter.

# Datatype

Integer

# Units

- checks

# Constraints

- Non-negative integer suppression count according to the setter specification.

# Inferred default

`2`.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: scheduling, cross-cluster-replication

# Notes

This is the Erlang application environment key `ttaaefs_autocheck_suppress_count` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_ttaaefs_manager.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_ttaaefs_manager.erl#L1009)

# Reviewed against

3.4.0: a319667bbcea2b5999e5a362e590c4da300a6395adf744e02e6fe9b819edb26d
3.4.1: 5d452be653efe3a0d42fe13df8fce8a7f78a049f8033ecb651f084b122019cbe
