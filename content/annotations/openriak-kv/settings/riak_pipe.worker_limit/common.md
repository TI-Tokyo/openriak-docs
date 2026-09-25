# Description

Maximum number of Riak Pipe workers allowed on each pipe vnode. The value must be a positive integer and bounds concurrent pipeline work on that partition.

# Datatype

Integer

# Units

- workers

# Constraints

- Validated as an integer greater than zero.

# Inferred default

`50`.

# Tags

feature: query-processing
repository: riak_pipe
module: riak_pipe_vnode
concept: concurrency, querying

# Notes

This is the Erlang application environment key `worker_limit` in `riak_pipe`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_pipe/src/riak_pipe_vnode.erl](https://github.com/OpenRiak/riak_pipe/blob/578c0c7304b11c564b894bcef1c3ded4459ef93b/src/riak_pipe_vnode.erl#L180)

# Reviewed against

3.4.0: e4ddf7777442517fba0afe40a70ce772dfbf1926b1666109394522cad22cfe98
3.4.1: e4ddf7777442517fba0afe40a70ce772dfbf1926b1666109394522cad22cfe98
