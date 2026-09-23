# Description

Certificate file used to encrypt intra-cluster handoff traffic. It may include the private key, or the key can be supplied separately through `handoff.ssl.keyfile`; these settings are separate from HTTPS certificates.

# Tags

feature: handoff
repository: riak_core
module: riak_core.schema
concept: partition-transfer, tls

# Reviewed against

3.4.0: 97b64a4e95d60ba3cfd7da60eca0f2a49f42b00b25a9a21b955f6a86a8887876
3.4.1: f92a8eb8d774a92826d524a5ccb1f3280f258e3ca0546cc255c3722b2860b453
