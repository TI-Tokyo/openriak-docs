# Description

Number of Tictac full-sync checks per day focused on recently modified data from the last day. For n_val sync, tree comparison still covers all data while repair discovery is time-limited; older divergence needs a broader check.

# Tags

feature: full-sync
repository: riak_kv
module: riak_kv_ttaaefs_manager
concept: replica-repair

# Reviewed against

3.4.0: 89032d8279e1dbc3b532f5420865f88fd43c0f51f2c91034984fb1ec000edd3f
3.4.1: 0464b3f34d537951d047b9b695d4b95a5e5f4551b28ab3c419e4694dbf9f4baa
