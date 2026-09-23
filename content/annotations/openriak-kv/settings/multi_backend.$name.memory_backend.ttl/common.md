# Description

For the named backend `$name`: Lifetime assigned to values written to the memory backend. Once expired, an object is removed on the next read of its key; this differs from a background disk-retention policy. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: memory-backend
repository: riak_kv
module: riak_kv.schema
concept: memory, retention, storage

# Reviewed against

3.4.0: 136f1067eae2658651e822dded3867d6f2e8970e66900df268a1f4eeb97e9cd0
3.4.1: 6ecdcbf3278cfc10c021d12c011a93d876f4b281babcd7a59e46dcfcdf535f48
