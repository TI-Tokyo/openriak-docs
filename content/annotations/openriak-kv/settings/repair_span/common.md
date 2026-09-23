# Description

Choose a pair or double pair of vnode sources for partition repair. `double_pair` requires sufficient replicas and should be paired with deferred fetching on a supporting backend, or overlapping source scans can duplicate much of the disk work.

# Tags

feature: handoff
repository: riak_core
module: riak_core_vnode_manager
concept: partition-transfer

# Reviewed against

3.4.0: f4a8e3a49591513a8a8d00f407986002146688004c26aa55ca927fa8fcc90a12
3.4.1: bdac8682e46dbd9ad8011fa54b370ebd777f18bff31f4787f49827521723c1ce
