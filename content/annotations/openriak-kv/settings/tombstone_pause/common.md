# Description

Pause in milliseconds between eraser deletes or reaper operations. It limits bulk-operation pressure and gives tombstones additional time to propagate before a timed deletion policy can reap them.

# Tags

feature: deletion
repository: riak_kv
module: riak_kv_delete, riak_kv_reaper
concept: tombstones

# Reviewed against

3.4.0: 5da4f078b0032f9b004875b421c0c3861334453bb192ecbced7a838dcc3b60ee
3.4.1: 4756b0f98532020f3a4102ea87eaee5115f44d87bc50e98ea7b8db9fbf39fc93
