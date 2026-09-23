# Description

Make legacy AAE tree rebuilds participate in shared background-resource management. This coordinates rebuild pressure with other participating tasks when `background_manager` is enabled.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: replica-repair

# Reviewed against

3.4.0: b203c0616e6d0ddb2c94797f3103ddc9188aed806379681f1641434fe61d3afe
3.4.1: cdc5dd0e611202f41c0361a1104e412905261110f95dfa7403366b58031b2140
