# Description

Select whether Tictac active anti-entropy runs for KV vnodes. Active operation maintains and compares trees to find divergent replicas; this switch is independent of the legacy `anti_entropy` setting.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_tictacaae_cli, riak_kv_vnode
concept: replica-repair

# Reviewed against

3.4.0: ee3a7abb17e2d966e1f0e132d32e5ef605387f14b1c514f745fb85dc953b183b
3.4.1: ff910f666299d6f694611dadf5e64fb66500cb658564e817b4a5d552477095cc
