# Description

How long normal schedulers spin for work before sleeping. Reducing busy waiting can lower idle CPU consumption; measure wakeup latency and throughput before changing it for a production workload.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime, scheduling

# Reviewed against

3.4.0: f21d4a4d434d6a69c17529a37c951090f296dfd4188b1efb46d2aa983189fb65
3.4.1: f21d4a4d434d6a69c17529a37c951090f296dfd4188b1efb46d2aa983189fb65
