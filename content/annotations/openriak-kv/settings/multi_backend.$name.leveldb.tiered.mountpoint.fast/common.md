# Description

For the named backend `$name`: Filesystem path for LevelDB levels below the tier boundary. Used with `leveldb.tiered` and the slow-tier path; changing the path alone does not relocate existing SST files. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: 292cc87aa1cbb570b31458556456812c0c10618cff26aabc702a862a83a4627a
3.4.1: 292cc87aa1cbb570b31458556456812c0c10618cff26aabc702a862a83a4627a
