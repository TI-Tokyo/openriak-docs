# Description

Choose the file-I/O implementation used by Bitcask. `erlang` uses the Erlang file API; `nif` calls the POSIX API directly. NIF I/O can improve throughput for some workloads but can also increase worst-case VM latency.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_io
concept: storage

# Reviewed against

3.4.0: c2b18ff204c583ea4a29bbc7773aa211565a7cd48310d1a79e2cf0e12ae4dbb9
3.4.1: c2b18ff204c583ea4a29bbc7773aa211565a7cd48310d1a79e2cf0e12ae4dbb9
