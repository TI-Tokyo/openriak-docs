# Description

Local IP address on which the node accepts intra-cluster handoff traffic. Peers must reach this interface and `handoff.port`; this listener is separate from distributed Erlang and client APIs.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_listener
concept: partition-transfer

# Reviewed against

3.4.0: b6d06dc74b31403e8ada9e26d013f669e6c7b46f2e52f8b239bd3e04a4803152
3.4.1: e53f507573e9bb7609787165fe0dddc1a454835cedf078d8f6f18e7537266592
