# Description

Use the operating-system WILLNEED file-access hint instead of DONTNEED for LevelDB. It can help when physical memory can hold the database, but changes page-cache pressure for the rest of the node.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: storage

# Reviewed against

3.4.0: 07d33740a39b63f316417afeadf574862af061ce505aa1e19cb426cff9905ed6
3.4.1: 07d33740a39b63f316417afeadf574862af061ce505aa1e19cb426cff9905ed6
