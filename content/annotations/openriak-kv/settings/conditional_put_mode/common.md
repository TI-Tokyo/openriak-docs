# Description

Choose how conditional PUT checks are enforced. `api_only` checks before writing and can race with another writer; `prefer_token` uses token coordination where supported. The documented `mandate_token` mode is not implemented; do not treat conditional PUTs as a general transaction mechanism.

# Tags

feature: conditional-writes
repository: riak_kv
module: riak_kv_pb_object, riak_kv_wm_object
concept: concurrency-control

# Reviewed against

3.4.0: d2e825b1151d23af27683ac6877813ca0f88eacdaad00fd17d706df73948633d
3.4.1: fa350ba5e3ffab2e09b85e7d0789aa7bb1f9eb1f835bffcf58f4362a3892a905
