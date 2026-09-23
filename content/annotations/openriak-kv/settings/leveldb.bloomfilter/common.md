# Description

Add Bloom filters to LevelDB SST files to avoid unnecessary reads for absent keys. Filters consume some additional storage and memory while improving negative-lookup efficiency.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: storage

# Reviewed against

3.4.0: 38ff49bf0655d2ec7f11ab4b7a77811e3d6eeeb8de16419fe7724c16143df8c1
3.4.1: 38ff49bf0655d2ec7f11ab4b7a77811e3d6eeeb8de16419fe7724c16143df8c1
