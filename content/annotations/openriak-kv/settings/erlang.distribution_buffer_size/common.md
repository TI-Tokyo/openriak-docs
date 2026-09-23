# Description

Sender-side buffer for distributed Erlang traffic. A larger buffer can reduce busy-distribution-port stalls, but permits more queued data and memory use when a peer cannot keep up.

# Tags

feature: erlang-runtime
repository: cuttlefish, riak
module: erlang_vm.schema, riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: 68353b60340398f7dfb7ce86aed3bd5eb306b03b9822595d17143bf5fb3734c9
3.4.1: 68353b60340398f7dfb7ce86aed3bd5eb306b03b9822595d17143bf5fb3734c9
