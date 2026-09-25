# Description

Property list containing the CA certificate, server certificate and private-key paths used to construct client-facing TLS options. The API TLS helper combines these credentials with its protocol, cipher and certificate-validation settings.

# Datatype

List

# Constraints

- SSL property list, including `{cacertfile, Path}`, `{certfile, Path}` and `{keyfile, Path}`; paths must refer to suitable certificate/key files.

# Inferred default

No fallback at this read. The SSL configuration is assembled from configured certificate/key settings.

# Tags

feature: security
repository: riak_api
module: riak_api_ssl
concept: authentication, tls

# Notes

This is the Erlang application environment key `ssl` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_api/src/riak_api_ssl.erl](https://github.com/OpenRiak/riak_api/blob/ffdbd6be1afd3e2350eee99dc96930f7b339c3bf/src/riak_api_ssl.erl#L35)

Additional type/default evidence:

- [riak_core/priv/riak_core.schema](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/priv/riak_core.schema)

# Reviewed against

3.4.0: fdb36d1e29cc2038c0dcc5e8dd35e39b713049635a6d062f42cc486579a1a808
3.4.1: 932c03edde874090adc603f8564604a0b85bd4b30ad89836118f6b540d88df49
