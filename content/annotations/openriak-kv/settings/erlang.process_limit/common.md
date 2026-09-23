# Description

Maximum number of Erlang processes in the node VM. Leave headroom for request coordinators and background work; request admission is separately controlled by `max_concurrent_requests`.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: runtime

# Reviewed against

3.4.0: 4d5dbd9f1fe3b455684013e0e47da1745cf978b0ffc4691eb885b3e605843fae
3.4.1: 4d5dbd9f1fe3b455684013e0e47da1745cf978b0ffc4691eb885b3e605843fae
