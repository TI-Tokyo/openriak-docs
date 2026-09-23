# Description

Initial process heap size in words. `otp` uses the runtime default. Raising it can reduce early heap growth for busy processes but multiplies the initial memory cost across many processes.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: 7b0d0ba9d7a0591fcfbd9ef4eb1227e5f1b732060408fecf8708612977154421
3.4.1: 7b0d0ba9d7a0591fcfbd9ef4eb1227e5f1b732060408fecf8708612977154421
