# Description

Additional directories added to the Erlang code path for custom modules and used by the code-reload command. With security enabled, these directories also define the permitted locations for custom MapReduce module functions.

# Datatype

List

# Constraints

- List of directory path strings.

# Inferred default

`[]` from `riak_kv.app.src`; no extra code paths.

# Tags

feature: query-processing
repository: riak_kv
module: riak_kv_app, riak_kv_console, riak_kv_util
concept: filesystem-layout, querying

# Notes

This is the Erlang application environment key `add_paths` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_app.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_app.erl#L79)
- [riak_kv/src/riak_kv_console.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_console.erl#L306)
- [riak_kv/src/riak_kv_util.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_util.erl#L584)

Additional type/default evidence:

- [riak_kv/src/riak_kv.app.src](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv.app.src)

# Reviewed against

3.4.0: d5ade0259f5a80870f25a3a70442b56613e1a0f0cb98004815135503b1355a6e
3.4.1: 7078775a0771e4337d2f4975d997e8c58f8bd6efaddc501c940e27d703d32d23
