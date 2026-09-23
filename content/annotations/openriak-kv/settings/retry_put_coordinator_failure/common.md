# Description

Retry a PUT when forwarding to a replica-local coordinator fails. Disabling this restores the older failure behaviour and can expose clients to transient coordinator-forwarding failures.

# Tags

feature: request-processing
repository: riak_kv
module: riak_kv_put_fsm
concept: overload-protection

# Reviewed against

3.4.0: fe00da01be883cfd2b3bba12f875df5d4a64651d65ac4a6f9d41f4a5855e3f0d
3.4.1: a604b31467b7a4e7618a7c3780fbc6bc3cfa3ff0c84e0e93b6f47bd6e4cd187f
