# Description

For the named backend `$name`: Filesystem path for LevelDB levels at or above the tier boundary. Used when tiering is enabled; existing level files must remain in the locations the configured layout expects. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: storage

# Reviewed against

3.4.0: fc65de01a0b3dcbe4952ee4e40f1d1a60f7a6bc53b7c24594a30e655bc0a19a8
3.4.1: fc65de01a0b3dcbe4952ee4e40f1d1a60f7a6bc53b7c24594a30e655bc0a19a8
