# Description

Interval in milliseconds between each vnode's prompts to start another Tictac AAE exchange. Lower values increase comparison frequency and background work. The source requires the vnode inactivity timeout to remain below half this interval to avoid obstructing handoff.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair, scheduling

# Reviewed against

3.4.0: f10cae32ff8892200a1c330f24d5c9e78e61c1d949bd0b8c8b25969f000d5a15
3.4.1: 4022e3760887f56ec1219d1a2328c0e57ae76a10bbab76c63b16318b1be76d74
