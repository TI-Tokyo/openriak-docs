# Description

Maximum object count in a handoff batch. Smaller batches let backpressure take effect sooner and are the first adjustment to consider for acknowledgement timeouts; they may increase per-batch overhead.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: partition-transfer

# Reviewed against

3.4.0: 625fad11c527782b10c5f0cf7cfb4fe04e84576c1c9d642ba70cb5316ab91b14
3.4.1: 18771027ed7a93fc0151763f308a05d537ba3a3587b1d9d6987c414d26595247
