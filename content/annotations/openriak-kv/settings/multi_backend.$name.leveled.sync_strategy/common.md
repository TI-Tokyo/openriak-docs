# Description

For the named backend `$name`: Choose how Leveled flushes writes to disk. `none` lets the operating system schedule flushing; `sync` and `riak_sync` synchronize each PUT using their respective mechanisms. Per-write synchronization trades latency and throughput for persistence. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveled
repository: leveled
module: leveled_multi.schema
concept: storage

# Reviewed against

3.4.0: 2824bccf50b04aa488a2a0fa06d8cb850acc3b1036a89966698ba16387492ec1
3.4.1: 609fc9b3edc1556b505f8480a1988eaa9560adaf5632740571a28c10e6786a0c
