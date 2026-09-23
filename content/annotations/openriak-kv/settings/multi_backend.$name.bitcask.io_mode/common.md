# Description

For the named backend `$name`: Choose the file-I/O implementation used by Bitcask. `erlang` uses the Erlang file API; `nif` calls the POSIX API directly. NIF I/O can improve throughput for some workloads but can also increase worst-case VM latency. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: storage

# Reviewed against

3.4.0: 3e6ab61cf005cf74079e58dda13f6b34dc0bdc6fc431138f8c875de6d2746804
3.4.1: 3e6ab61cf005cf74079e58dda13f6b34dc0bdc6fc431138f8c875de6d2746804
