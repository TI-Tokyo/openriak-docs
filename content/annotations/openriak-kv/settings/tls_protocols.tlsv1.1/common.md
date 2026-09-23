# Description

Allow `tlsv1.1` during TLS protocol negotiation. Each protocol has its own switch, and the installed OTP TLS implementation must support it. This is a legacy protocol; enable it only for a specifically understood compatibility requirement.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication, tls

# Reviewed against

3.4.0: cc7942e2dfda6128c7759893bdf01fa9547931a761d83625d0830e5fae4cd650
3.4.1: 7cadb968566801806d9355b89e5b1e628a5011fe9a21834f3e0acf21ad47b9e7
