# Description

Delay, in milliseconds, between LevelDB open attempts after a database-lock error. It gives a previous backend instance time to finish releasing its native resources.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a non-negative integer sleep duration.

# Inferred default

`2000`.

# Tags

feature: leveldb
repository: riak_kv
module: riak_kv_eleveldb_backend
concept: scheduling, storage

# Notes

This is the Erlang application environment key `eleveldb_open_retry_delay` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_eleveldb_backend.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_eleveldb_backend.erl#L706)

# Reviewed against

3.4.0: 7e76e88352a4521ba481cea10410c92165391316e3a79b324bf7da2c925c14c3
3.4.1: 7bee73f7cdeef6913faa05e2311105132962d2e81d4034386b4e17a9c04a3233
