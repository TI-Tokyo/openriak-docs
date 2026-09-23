# Description

Allow `tlsv1` during TLS protocol negotiation. Each protocol has its own switch, and the installed OTP TLS implementation must support it. This is a legacy protocol; enable it only for a specifically understood compatibility requirement.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication, tls

# Reviewed against

3.4.0: a941befc6ba78b58a964630676100dd72d2d946ebe91ddfca37f8a406c3bd67b
3.4.1: 6ca7b6f0c26451af1af1a66f4ea837b969a9521c9e303b3802bfea645972abdf
