# Description

Initial binary virtual-heap threshold in words. It influences when binary allocation prompts garbage collection; `otp` leaves the value to the runtime. Larger thresholds can reduce collection frequency while retaining more memory.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: memory, runtime

# Reviewed against

3.4.0: 8ed5b5e8233c59654faad2da040284b65b9191397482e0d0640ba683bdc779af
3.4.1: 8ed5b5e8233c59654faad2da040284b65b9191397482e0d0640ba683bdc779af
