# Description

Local registered replication queue receiving references to objects needing full-sync repair. The queue must exist; it may also carry real-time replication work rather than being dedicated to full-sync.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: queueing, replica-repair

# Reviewed against

3.4.0: 20535b7c94fd01f844422ab4495d2c976319ac1dd1ea7060e1cfaa0936dafdb4
3.4.1: 727d1b38a08fd1cc97b7cfa3addda89f03c02501872f85512b088c9e97e9b60c
