# Description

Allow `tlsv1.2` during TLS protocol negotiation. Each protocol has its own switch, and the installed OTP TLS implementation must support it. Peers must have an enabled protocol in common for the TLS handshake to succeed.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication, tls

# Reviewed against

3.4.0: 514958e3fb0666342645df9c0fca75dc4a389cff2e563da149729bdf3c41acec
3.4.1: 9afdf39ed74fe6e8108a3c8a2dea82e1af07962b456f72b121c96fbcf55f220b
