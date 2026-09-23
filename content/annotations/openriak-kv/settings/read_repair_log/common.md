# Description

Log each key repaired while processing reads. This helps trace replica divergence, but can produce substantial log volume during recovery or widespread inconsistency.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_get_fsm
concept: diagnostics, replica-repair

# Reviewed against

3.4.0: 344687e6d7c2f19c2a367f04ceae60f983afa4cc617828b4666fd826003bd3d5
3.4.1: e50e56ad36bfb8556e94563bdaf357a91cfbbd36ca6e57a6d5c00ac2028a8330
