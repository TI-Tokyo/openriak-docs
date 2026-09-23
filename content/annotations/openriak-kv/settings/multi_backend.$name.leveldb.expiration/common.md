# Description

For the named backend `$name`: Enable backend-level expiry for LevelDB data. Configure the retention period and expiry mode separately; named multi-backend instances can have their own retention settings. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: retention, storage

# Reviewed against

3.4.0: 6902b1be46c17e7c622917d321b6584235594c60d793e15ffeeef00698a1a4ef
3.4.1: 6902b1be46c17e7c622917d321b6584235594c60d793e15ffeeef00698a1a4ef
