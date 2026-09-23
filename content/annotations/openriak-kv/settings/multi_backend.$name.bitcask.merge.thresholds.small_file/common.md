# Description

For the named backend `$name`: Files smaller than this size are eligible for a Bitcask merge even without meeting other inclusion thresholds. Raising it includes more small files; it does not itself define the dead-data trigger. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: bitcask
repository: bitcask
module: bitcask_multi.schema
concept: compaction, storage

# Reviewed against

3.4.0: 6bc816ca137225469312117b1283f66e235aea98262f4297ba100a84dd7cd17d
3.4.1: 6bc816ca137225469312117b1283f66e235aea98262f4297ba100a84dd7cd17d
