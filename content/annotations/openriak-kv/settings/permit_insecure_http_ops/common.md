# Description

Compatibility switch allowing selected statistics, AAE-fold and replication-fetch operations over unauthenticated HTTP when security is enabled. Without it, these operations require HTTPS and an authorized user. Enabling it restores the older exposure for those endpoints.

# Tags

feature: security
repository: riak_kv
module: riak_kv_wm_aaefold, riak_kv_wm_queue, riak_kv_wm_stats
concept: authentication

# Reviewed against

3.4.0: 7b7027f838546db733e8677715565cc984e60c6a03efbfa164b696a86d9abc07
3.4.1: 71600723e2615a93a312ccaa9b1ff1534dce25dde8f40fd13df61b2fd7314930
