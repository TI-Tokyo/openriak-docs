# Description

Delay applied by a legacy AAE throttle tier. Replace `$tier` with the same name used in its `mailbox_size` setting; a larger delay reduces AAE pressure once that queue threshold is reached.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: replica-repair, retention, scheduling

# Reviewed against

3.4.0: 3e0bea0412f40fbf92c41295f77fc7ac83f456a10d00e668668d7d556a678e16
3.4.1: 248ecf6c4539e3000ae001c914bf75148929c35c1ae88fb4217876af5e7a1c10
