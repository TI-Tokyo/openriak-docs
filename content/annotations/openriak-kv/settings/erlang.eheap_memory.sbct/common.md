# Description

Single-block carrier threshold for the Erlang process-heap allocator, in kilobytes. Allocations above this threshold use individual carriers instead of sharing multi-block carriers.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: bc0314126dc639829fa20610f298acaf15700164f7dd0ffec27c5b69c1d478ef
3.4.1: bc0314126dc639829fa20610f298acaf15700164f7dd0ffec27c5b69c1d478ef
