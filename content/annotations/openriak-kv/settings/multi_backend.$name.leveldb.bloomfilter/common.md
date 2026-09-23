# Description

For the named backend `$name`: Add Bloom filters to LevelDB SST files to avoid unnecessary reads for absent keys. Filters consume some additional storage and memory while improving negative-lookup efficiency. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: f652671d2e0c71ba4e74ea729b8115e79eee6438dcd97b8cfa537bfb9fb88f1a
3.4.1: f652671d2e0c71ba4e74ea729b8115e79eee6438dcd97b8cfa537bfb9fb88f1a
