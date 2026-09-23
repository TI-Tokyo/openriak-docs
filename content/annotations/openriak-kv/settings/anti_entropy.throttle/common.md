# Description

Enable load-dependent throttling of legacy active anti-entropy. Configure matching mailbox-size and delay entries under `anti_entropy.throttle.$tier` to slow repair when vnode queues grow.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: replica-repair, retention

# Reviewed against

3.4.0: 1793288d906b9191459f9ca259ce2b0e3589187b39ccb829bc169c018f61d0d2
3.4.1: aa3871f1efa2c89ff337d4ba86f19b4ce187a4fa2e42b200da056e6a7c6e5391
