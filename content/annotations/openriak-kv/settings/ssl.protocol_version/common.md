# Description

TLS protocol-version list consulted by Ranch when its socket options do not explicitly specify `versions`. If this application value is also absent, Ranch uses the protocols reported as supported by the Erlang SSL application.

# Datatype

List

# Constraints

- List of TLS version atoms supported by the installed SSL runtime, such as `'tlsv1.2'`; this consumer does not define a fixed, version-independent set.

# Inferred default

The supported protocol list reported by `ssl:versions()` for the installed Erlang/SSL runtime.

# Tags

feature: security
repository: ranch
module: ranch_ssl
concept: tls

# Notes

This is the Erlang application environment key `protocol_version` in `ssl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [ranch/src/ranch_ssl.erl](https://github.com/OpenRiak/ranch/blob/4184efa50ade7879475b288c3339627052a254a8/src/ranch_ssl.erl#L338)

# Reviewed against

3.4.0: bffc3f27de9fd295c5fdaa59512d508de5e8b183c06af2a979fa01b76a38a3ca
3.4.1: bffc3f27de9fd295c5fdaa59512d508de5e8b183c06af2a979fa01b76a38a3ca
