# Description

For the named backend `$name`: Directory under which Bitcask stores partition data files and hint files. Ensure the Riak service account can write it and include it in storage-capacity and backup planning. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: filesystem-layout, storage

# Reviewed against

3.4.0: 0a8023e31a61a9e7c3e4a0faf49e327e17412a58bcdb17348da78929a884a36b
3.4.1: 0a8023e31a61a9e7c3e4a0faf49e327e17412a58bcdb17348da78929a884a36b
