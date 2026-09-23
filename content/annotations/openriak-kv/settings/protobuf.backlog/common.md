# Description

Maximum queue of pending connections awaiting acceptance by the Protocol Buffers listener. Increase it for bursts of simultaneous connection establishment; it does not increase the number of active request workers.

# Tags

feature: client-networking
repository: riak_api
module: riak_api_pb_listener
concept: connections, diagnostics

# Reviewed against

3.4.0: bd8936d59601f93aaeb2a70991a1004444c64e5dcbf761c7786238ed02db6cc1
3.4.1: 52b04da2604364584876f56a060095dfd55de179752089ae639355e949691411
