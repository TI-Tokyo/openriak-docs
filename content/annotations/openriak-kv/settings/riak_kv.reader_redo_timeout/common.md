# Description

Retry-queue pause, in milliseconds, supplied by the background reader to the shared queue manager. The built-in read action reports completion even when the GET result is an error, so this does not by itself retry every failed read.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a positive integer.

# Inferred default

`2000`.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_reader
concept: scheduling, replica-repair

# Notes

This is the Erlang application environment key `reader_redo_timeout` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_reader.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_reader.erl#L114)

# Reviewed against

3.4.0: 820d2f4b45dd256b67e8aff9a385eca240a5dd60f4e3ac895a1945b7f24ba1a4
3.4.1: 44826c235b9e33520262a198860e5505dbbe959123afba96bcfe16b8c493f80b
