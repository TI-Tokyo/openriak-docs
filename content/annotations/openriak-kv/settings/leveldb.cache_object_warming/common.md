# Description

Save cache information, currently open SST filenames, when closing a database and use it on the next open. This can reduce initial request latency by reopening those files before client reads need them.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb.schema
concept: memory, storage

# Reviewed against

3.4.0: 154aa082b6cf2f44e17ad851645d8734b83a6d54cb613b053f3db8b5876166d3
3.4.1: 154aa082b6cf2f44e17ad851645d8734b83a6d54cb613b053f3db8b5876166d3
