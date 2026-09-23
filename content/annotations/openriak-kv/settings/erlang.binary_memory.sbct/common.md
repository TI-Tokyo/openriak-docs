# Description

Single-block carrier threshold for the Erlang binary allocator, in kilobytes. Allocations above this threshold use individual carriers instead of sharing multi-block carriers.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: b545962ca40ef24521560b01a1155743f1b824a1957d142ea2a18c6a65a37c6d
3.4.1: b545962ca40ef24521560b01a1155743f1b824a1957d142ea2a18c6a65a37c6d
