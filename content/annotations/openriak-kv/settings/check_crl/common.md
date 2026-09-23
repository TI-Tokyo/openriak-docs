# Description

Check client certificates against certificate revocation lists during TLS verification. Disabling this permits use with certificate authorities that lack usable CRLs, but removes that revocation check.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication

# Reviewed against

3.4.0: 4d0a78de06dc37dc08c4bf6371762cfcfb31f924da393e4b2e86be9c5f714983
3.4.1: 4406013241f693b2c517c0ab4b3d6a0107c660dcc0a744f2f668cc874cce41fe
