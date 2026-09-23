# Description

JSON encoder used for secondary-index results. The OTP-derived encoder improves large-result encoding performance; selecting the legacy encoder can preserve older output ordering, although JSON object-key order is not a data contract.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_kv_wm_index
concept: querying

# Reviewed against

3.4.0: 33679dce969c7d46c0af51c6c6b71d5bc0e66e52678e7fe14dd7c41ee7d93738
3.4.1: ac631b84ce93074b2ccec095cd0a9a4c919febf3bf68dea53a5a238935d9443a
