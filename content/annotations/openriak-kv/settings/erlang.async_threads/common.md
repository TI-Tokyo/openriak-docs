# Description

Size of the Erlang asynchronous driver thread pool. This pool is distinct from scheduler threads and Riak worker pools; tune it for drivers that use asynchronous work.

# Tags

feature: erlang-runtime
repository: cuttlefish, riak
module: erlang_vm.schema, riak.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: 537516d885b6182abb62d155309a455a4eebde271dc8ac170306964355ab0c10
3.4.1: 537516d885b6182abb62d155309a455a4eebde271dc8ac170306964355ab0c10
