# Description

Enable Bloom filters in the LevelDB store used for legacy AAE hash trees. Filters reduce unnecessary disk lookups for absent keys, at the cost of filter storage; this does not configure the user-data backend.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: replica-repair

# Reviewed against

3.4.0: 457b3817c1c9dc175c45ebf413b1f95439eaf334948109c4f7d0b5c0a20ff46a
3.4.1: 75b41c4c51cab7831682b42a1f90b71668aa0cc0a0514e3a377d2b6d0639568f
