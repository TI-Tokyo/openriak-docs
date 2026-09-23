# Description

Allow `sslv3` during TLS protocol negotiation. Each protocol has its own switch, and the installed OTP TLS implementation must support it. This is a legacy protocol; enable it only for a specifically understood compatibility requirement.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication, tls

# Reviewed against

3.4.0: a6a35b4a1d410255abbf4aad441c73dbdea9947910c7fad88021bd72fcd50ec2
3.4.1: 3ca1787b1168f51cb4a6f18c66ddd4c6e37361926950540a57b25de7ed77d36a
