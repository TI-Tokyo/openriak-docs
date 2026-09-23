# Description

Timeout in milliseconds for executing a secondary-index query and collecting results. Zero disables it. JSON encoding time is outside this timeout; an HTTP query hitting the limit returns a 503 response.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_index
concept: querying, scheduling

# Reviewed against

3.4.0: 574b39ca3c37b2b92ebaa9b2d11334853e2ab6f82d3c0054f6f82bf7afcdc764
3.4.1: 18016d3385bfdf70488e626e67f410384f7d457010e69c9a0cfb9ac3f27e62d0
