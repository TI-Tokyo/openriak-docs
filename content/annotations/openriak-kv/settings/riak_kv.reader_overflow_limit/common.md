# Description

Maximum number of background-reader references allowed in the disk overflow queue. It bounds spillover beyond the reader's in-memory queue; further work may be discarded when capacity is exhausted.

# Datatype

Integer

# Units

- references

# Constraints

- Expected to be a positive integer.

# Inferred default

`10000000`.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_reader
concept: queueing, replica-repair

# Notes

This is the Erlang application environment key `reader_overflow_limit` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_reader.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_reader.erl#L118)

# Reviewed against

3.4.0: d70c6e8845f92181273ff1e5d7ad9a8a1b20e30b7c17633049a9ec704f3a8dc0
3.4.1: 6692bad976f722d7193fee533a2b1745077da35ffe663f2f1be660ff3e37d4d0
