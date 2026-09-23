# Description

Replica acknowledgement requirement for queue-replication fetches and pushes. `one` minimizes work; `quorum` or `all` waits for more replicas and can reduce later repair work when individual vnodes are under pressure.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_client
concept: cross-cluster-replication

# Reviewed against

3.4.0: 29bf9bfdcb7c467b3a7ceb422eceff3ec76916087811ec0d865a960a5dc0cfaa
3.4.1: e9ba7515ff851fd4f029fa95eca278117691d2a8c81e00ca9dece53f0b10fc63
