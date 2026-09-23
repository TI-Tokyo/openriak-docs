# Description

Apply backpressure when the anti-entropy store falls behind vnode writes. The vnode periodically waits for AAE progress using Tictac pings or legacy hashtree synchronization, trading write throughput for a bounded AAE backlog.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair

# Reviewed against

3.4.0: 2c54ec05af334d3616ae0c64d36ce3119e20b0f57c9295713abe15c65c746868
3.4.1: 27243047ca59fd34e5823aeaad6235f9b8fd1c9b2bb3e0b64339b860b5ad5109
