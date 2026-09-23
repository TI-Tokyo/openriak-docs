# Description

Files smaller than this size are eligible for a Bitcask merge even without meeting other inclusion thresholds. Raising it includes more small files; it does not itself define the dead-data trigger.

# Tags

feature: bitcask
repository: bitcask
module: bitcask.schema
concept: compaction, storage

# Reviewed against

3.4.0: ddc6d94702aa97fd418ddaf27d42ed9fb703f36bcb753c5a087329187b2a58a5
3.4.1: ddc6d94702aa97fd418ddaf27d42ed9fb703f36bcb753c5a087329187b2a58a5
