# Description

Maximum input-queue length for an individual Riak Pipe worker. A fitting's effective queue limit is the smaller of this positive integer and the fitting's own `q_limit`.

# Datatype

Integer

# Units

- items

# Constraints

- Validated as an integer greater than zero.

# Inferred default

`4096`.

# Tags

feature: query-processing
repository: riak_pipe
module: riak_pipe_vnode
concept: queueing, querying

# Notes

This is the Erlang application environment key `worker_queue_limit` in `riak_pipe`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_pipe/src/riak_pipe_vnode.erl](https://github.com/OpenRiak/riak_pipe/blob/578c0c7304b11c564b894bcef1c3ded4459ef93b/src/riak_pipe_vnode.erl#L185)

# Reviewed against

3.4.0: f228abe2547d0b7c42a1a9b6d72dcce5bf78590c82cf6b8061718812d7f79c9a
3.4.1: f228abe2547d0b7c42a1a9b6d72dcce5bf78590c82cf6b8061718812d7f79c9a
