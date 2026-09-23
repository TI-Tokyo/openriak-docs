# Description

Control the Erlang `global` subsystem's overlapping-partition prevention. Riak is designed to tolerate network partitions; enabling this prevention can disrupt normal cluster changes when nodes learn about membership at different times.

# Tags

feature: erlang-runtime
repository: riak_core
module: riak_core.schema
concept: runtime

# Reviewed against

3.4.0: 4b778f70e5106c17f84a6d5a39ea441b4f1f119bed3bcfe09df3cf3b16c2b422
3.4.1: b07ed95d79a5d134c3f4b2538362febf04e31f6b8d84ead7bc6f90c5a1d3b139
