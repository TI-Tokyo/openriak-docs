# Description

Number of general query workers per vnode. Secondary-index and legacy list queries share this pool; Tictac rebuilds may also use it, and AAE folds use it when no node-wide strategy is enabled. Monitor queue time before raising concurrency.

# Tags

feature: worker-pools
repository: riak_kv
module: riak_kv_vnode
concept: background-work, concurrency

# Reviewed against

3.4.0: a538dd2305c62fe62ab6f9c9d546941d2a07aec7eeea433c72d50791ddf0163c
3.4.1: a6b2613d443eeae00b775797a4366466d9e1ab687eee9b61ce1866ed01c28fe6
