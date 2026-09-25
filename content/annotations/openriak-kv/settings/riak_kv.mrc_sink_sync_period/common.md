# Description

Number of asynchronous sends a pipeline worker makes between synchronous sends to the MapReduce sink. These periodic acknowledgements provide backpressure; `infinity` disables synchronous sends. This is a message count, not a duration.

# Datatype

Integer or atom

# Units

- messages

# Constraints

- An integer synchronization period, or `infinity` to disable periodic synchronous delivery. Positive integers describe useful message-count periods.

# Inferred default

`10`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_mrc_pipe
concept: queueing, querying

# Notes

This is the Erlang application environment key `mrc_sink_sync_period` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_mrc_pipe.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_mrc_pipe.erl#L979)

# Reviewed against

3.4.0: 65894c7e3cd0950e6709b7124d67c1d2b5b4c0556bd130ef8cdf14571ba2b082
3.4.1: 687bfd88e108a7ade3dfc6089617b2722e4cb3e4e7ba0f132f9e126f689d4142
