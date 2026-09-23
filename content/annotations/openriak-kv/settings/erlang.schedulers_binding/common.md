# Description

Control whether scheduler threads are bound to CPUs. Binding can interfere with other work on the host; verify the actual result with `erlang:system_info(scheduler_bindings)` because binding requires a detectable CPU topology.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: a9aeac9462ba9b9b43db838373e215f73cf9b400ce4ece41a4b9005210a28630
3.4.1: a9aeac9462ba9b9b43db838373e215f73cf9b400ce4ece41a4b9005210a28630
