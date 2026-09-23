# Description

Store full object heads in a parallel Tictac key store so head-fold queries can use it. Disabling this reduces auxiliary-store cost but retains only the smaller data set needed for AAE and monitoring.

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_kv_vnode
concept: replica-repair

# Reviewed against

3.4.0: 53974f539b82dce85e2a66660b419806f5ca73614793c6b461f864535d1573e7
3.4.1: ec778366a711dff526130c3edf2519e7a2bcc5f06d8722571775caa4261a3321
