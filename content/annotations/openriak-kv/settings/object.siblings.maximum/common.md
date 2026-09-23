# Description

Sibling-count threshold above which an object write fails. This protects against unbounded conflict growth; use the warning threshold to detect problematic sibling accumulation before writes reach this limit.

# Tags

feature: object-storage
repository: riak_kv
module: riak_kv_vnode
concept: data-model

# Reviewed against

3.4.0: 2b6428226c909da4d66cda3ffcfead1e22426e19b561b72974518890bf483073
3.4.1: 66ae5ef613b6c9a7646dc47038a8d16ca98befdd326ff65747038098f897549b
