# Description

Trace categories supplied to Riak Pipe for MapReduce execution, with `[error]` as the source fallback. Selected pipeline log events are sent to the result sink.

# Datatype

List or atom

# Constraints

- List of Riak Pipe trace-category atoms (for example `error`), or `all` for all trace events. Categories are matched to emitted trace tags.

# Inferred default

`[error]`.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_mrc_pipe
concept: diagnostics, querying

# Notes

This is the Erlang application environment key `pipe_log_level` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_mrc_pipe.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_mrc_pipe.erl#L255)

Additional type/default evidence:

- [riak_pipe/src/riak_pipe_log.erl](https://github.com/OpenRiak/riak_pipe/blob/578c0c7304b11c564b894bcef1c3ded4459ef93b/src/riak_pipe_log.erl)

# Reviewed against

3.4.0: 1e08482bc23f2a2fb4b504391564f7b9b9bdbe3ad0014dec8f1ffb5adb7ebae1
3.4.1: f0df097f35e73abbea80a652246b5716831f7a9ce70a91ebb6097afca7fefd9a
