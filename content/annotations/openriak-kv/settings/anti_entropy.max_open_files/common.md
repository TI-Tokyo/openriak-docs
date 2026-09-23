# Description

Open-file limit for the LevelDB stores backing legacy AAE trees. Include these handles when sizing the node's operating-system file-descriptor limit; this is separate from the user-data backend configuration.

# Tags

feature: legacy-aae
repository: riak_kv
module: riak_kv.schema
concept: replica-repair

# Reviewed against

3.4.0: 12c547955edd67ee991705715f8cae141389c40480e850f9a44044543f9dbe96
3.4.1: 726662c7e77d0782ab3ca909cc690dcbb25413d3cd264ff94579fb201b63ee70
