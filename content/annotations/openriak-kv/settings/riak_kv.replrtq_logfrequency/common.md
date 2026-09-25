# Description

Interval, in milliseconds, between source replication queue log reports. The queue process reads it at initialization and uses it to reschedule queue reporting.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- Expected to be a positive integer.

# Inferred default

`30000`.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: diagnostics, cross-cluster-replication

# Notes

This is the Erlang application environment key `replrtq_logfrequency` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_replrtq_src.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_replrtq_src.erl#L347)

# Reviewed against

3.4.0: 37feaf3a588f964785be30be09f5b4b985813b49918bda4ef8cf54583f9dd526
3.4.1: ae00cf47466d6376629d157aa534f4c38f083e2e6f091b5e63a83f536971fa2c
