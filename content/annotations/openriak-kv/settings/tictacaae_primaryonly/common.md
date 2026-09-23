# Description

Limit Tictac AAE exchanges to primary vnodes. Disabling it also permits exchanges with fallback vnodes, increasing repair coverage and the work performed during failures.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair

# Reviewed against

3.4.0: a5a898fd3cc767eae7e004a3ea58bb48a3c73501588d1bd83689d89702032b03
3.4.1: 2804a28abdefc02ff4a475764f0b0f657613946115baffaae0973eac45b64e14
