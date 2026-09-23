# Description

Admission limit for concurrent GET coordinators and, separately, PUT coordinators. `infinite` disables this overload protection. The Erlang process limit needs additional headroom; the source guidance is at least three times this request limit.

# Tags

feature: request-processing
repository: riak_kv
module: riak_kv_app
concept: concurrency, overload-protection

# Reviewed against

3.4.0: 39ac637a325f04500620fc2161fed2b9f95199d2f2879018c9cd5f46c34f1e9b
3.4.1: 952f06a078fb2fecbcab89fa75156c28d0bcce516b86c4ff9600eda36a799e0d
