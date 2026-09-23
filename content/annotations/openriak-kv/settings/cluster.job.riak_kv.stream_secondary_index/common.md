# Description

Allow streaming secondary-index queries through the cluster job controls. Disabling this blocks that class of work; it does not delete stored data or change the backend's query capabilities.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_core_util
concept: query-admission, querying

# Reviewed against

3.4.0: 53da613fa1d3226c5c5f97a3c1c630023c26621fd04f6854b4c9cd830d878e00
3.4.1: 858a6a9720b93fa3d359d37b090480014aa33cd47e5f4ec5999cf45983ee1c74
