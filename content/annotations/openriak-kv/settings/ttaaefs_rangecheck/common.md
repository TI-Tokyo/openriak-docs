# Description

Number of range-limited full-sync checks per day. A range comes from a previous mismatch or the last successful check; no range check runs when divergence is known but no useful range has been found. N_val tree comparison still covers the full replica set.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 71de5bfcba73b66504b2b365a640dc12dbb5f87a2d8b83160a0e76a2132a67df
3.4.1: f3c557c5e2b039ff3a28391069eb5f080e932a95644969f326f2761b15b2bab5
