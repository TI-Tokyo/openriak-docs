# Description

In-memory queue limit for the background eraser, which deletes objects using their vector clocks. Additional queued work is handled by the worker's overflow queue and its separate overflow limit.

# Datatype

Integer

# Units

- references

# Constraints

- Expected to be a positive integer.

# Inferred default

`100000`.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_eraser
concept: queueing, tombstones

# Notes

This is the Erlang application environment key `eraser_queue_limit` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_eraser.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_eraser.erl#L139)

# Reviewed against

3.4.0: d5fb560e883289f49549fa6fd83ab11fdc54dbd369ca941b6b8439d93208908b
3.4.1: 6b86e82d94bb32572b07891be0a8ee0e9506e042d772f9f18a0947afc8991cf2
