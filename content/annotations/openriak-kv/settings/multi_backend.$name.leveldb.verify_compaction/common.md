# Description

For the named backend `$name`: Verify LevelDB data during compaction. This provides integrity checking while files are rewritten, with additional work on the compaction path. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 725f5e104d2753872057e0491b7009deb36ea9ea80a2b8cfedc615ad46970f55
3.4.1: 725f5e104d2753872057e0491b7009deb36ea9ea80a2b8cfedc615ad46970f55
