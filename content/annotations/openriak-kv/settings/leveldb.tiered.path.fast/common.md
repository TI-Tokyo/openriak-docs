# Description

Filesystem path for LevelDB levels below the tier boundary. Used with `leveldb.tiered` and the slow-tier path; changing the path alone does not relocate existing SST files.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: filesystem-layout, storage

# Reviewed against

3.4.0: 9a572f4ffb9627351ff19a64be5b5906ffa1456d07007df5f5a85845d4be3c6d
3.4.1: 9a572f4ffb9627351ff19a64be5b5906ffa1456d07007df5f5a85845d4be3c6d
