# Description

Check HTTP Referer headers as part of the protection against cross-site request attacks. Disable only when an understood proxy arrangement requires it; doing so removes that check from the affected requests.

# Tags

feature: security
repository: riak_kv
module: riak_kv_wm_utils
concept: authentication

# Reviewed against

3.4.0: e07c8ddbc90a7d9313c43fb9c6ab9b0cc978d0526029cc7f8de4beb46be417d3
3.4.1: f3d0761783307ec90f44c99b1834a59966818870f0b6fdd1ee74811a1028ae7c
