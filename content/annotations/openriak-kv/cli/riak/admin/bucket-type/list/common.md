# Metadata

command: shell:riak admin bucket-type list
versions: 3.4.0, 3.4.1

# Summary

List known bucket types and their activation state.

# Description

Only active types can be used for ordinary typed-bucket operations. Newly created types remain inactive until explicitly activated.

# Arguments

# Reviewed against

3.4.0: a59e2a50f9db6ace7d335f5f1752c32a94cf5d7e65aa805b9c3603f9b2501464
3.4.1: a59e2a50f9db6ace7d335f5f1752c32a94cf5d7e65aa805b9c3603f9b2501464

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv_console
concept: data-policy
