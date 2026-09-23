# Description

Lower bound of the randomly selected per-vnode LevelDB write-buffer size. New values enter this memory buffer alongside the recovery log before being flushed into SST files.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: memory, storage

# Reviewed against

3.4.0: 04b36946ad83bcf800efc5021c80a8d0c417f61167c5b8e488d5ce05e64ff281
3.4.1: 04b36946ad83bcf800efc5021c80a8d0c417f61167c5b8e488d5ce05e64ff281
