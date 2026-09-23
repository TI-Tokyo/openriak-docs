# Metadata

command: shell:riak admin bucket-type list
versions: 3.4.0, 3.4.1

# Summary

List known bucket types and their activation state.

# Description

Only active types can be used for ordinary typed-bucket operations. Newly created types remain inactive until explicitly activated.

# Arguments

# Reviewed against

3.4.0: eb5d4ca65615b79511f7b08d375ce8fae239d72beb6cc3e5396ffd49920e8ec8
3.4.1: eb5d4ca65615b79511f7b08d375ce8fae239d72beb6cc3e5396ffd49920e8ec8

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv_console
concept: data-policy
