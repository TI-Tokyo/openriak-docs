# Description

Token-bucket limit for ring gossip, expressed as `{TokenCount, ResetMilliseconds}`. The gossip process replenishes its tokens at each reset to bound how frequently it sends ring updates.

# Datatype

Tuple

# Constraints

- `{TokenCount, ResetMilliseconds}`: non-negative integer token count and timer delay. A positive reset delay avoids a tight reset loop.

# Inferred default

`{45, 10000}`.

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_gossip
concept: scheduling

# Notes

This is the Erlang application environment key `gossip_limit` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_gossip.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_gossip.erl#L131)

# Reviewed against

3.4.0: a516fdedf60401b9e1a18041546b259e15f48001dc06db8ae30457668ce1ba88
3.4.1: a516fdedf60401b9e1a18041546b259e15f48001dc06db8ae30457668ce1ba88
