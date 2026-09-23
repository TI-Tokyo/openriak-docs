# Description

Shared secret used to authenticate distributed Erlang connections between nodes. Cluster members must agree on the cookie. Treat it as a credential; changing it on only one node prevents that node from communicating with its peers.

# Tags

feature: erlang-runtime
repository: cuttlefish, riak
module: erlang_vm.schema, riak.schema
concept: runtime

# Reviewed against

3.4.0: 4ab91debf64515184b9e7bd04f3f7345df1b4cd84811f77b5daa90a4dee021a8
3.4.1: 4ab91debf64515184b9e7bd04f3f7345df1b4cd84811f77b5daa90a4dee021a8
