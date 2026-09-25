# Description

Maximum number of MapReduce results buffered by the sink before it applies backpressure to synchronous senders. A sink-specific `buffer` option takes precedence over this nonnegative integer.

# Datatype

Integer

# Units

- results

# Constraints

- Validated as an integer greater than or equal to zero. A query's `buffer` option takes precedence.

# Inferred default

`1000` if neither the query options nor the application environment provides a valid size.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_mrc_sink
concept: memory, querying

# Notes

This is the Erlang application environment key `mrc_sink_buffer` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_mrc_sink.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_mrc_sink.erl#L383)

# Reviewed against

3.4.0: e271aca8faa6563ff67e672330016322bc168b6857c49febd6ef7a502ed20a82
3.4.1: 90a54804afd9f9c8ef156331457406c47dd153275e06df2e310a18bbbfe70546
