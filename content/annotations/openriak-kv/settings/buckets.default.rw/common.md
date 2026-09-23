# Description

Default combined read/write quorum value used by delete operations on untyped buckets. It governs delete request acknowledgement, separately from how long the resulting tombstone is retained.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: data-policy, quorums

# Reviewed against

3.4.0: acd73405e3a35f73dee662adfe57dc0a0924cfa2b80bf082fe687bc2aa7f6694
3.4.1: 372df5a6f4cdf338735dd9b91b05472a7b77046148bcf70ea5714a8acfcc1b7f
