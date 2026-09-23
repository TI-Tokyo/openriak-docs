# Description

Age after which a legacy AAE hash tree expires and needs rebuilding. Periodic rebuilds compare tree state with backend data and can expose silent corruption, but frequent expiration adds full-partition scans.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv_index_hashtree
concept: replica-repair, retention

# Reviewed against

3.4.0: aa0b8c61e9685aece6880d4931cad527f1c982e5b3c1d9e04b6a321f23623487
3.4.1: 1424ece8a5d7df1ee1c44aedc6255bb13f01172d5829fb774174cf8d9853cc87
