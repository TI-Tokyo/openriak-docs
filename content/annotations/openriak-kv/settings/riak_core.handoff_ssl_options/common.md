# Description

TLS option list used for handoff connections, including certificate, private-key and CA file paths. An empty list selects plain TCP; the handoff code checks that configured credential files are readable before using the options.

# Datatype

List

# Constraints

- SSL option property list. Configured `certfile`, `keyfile`, `cacertfile` and `dhfile` paths are checked for readability; the SSL implementation validates the remaining options.

# Inferred default

`[]`, which disables TLS for handoff.

# Tags

feature: handoff
repository: riak_core
module: riak_core_handoff_sender
concept: partition-transfer, tls

# Notes

This is the Erlang application environment key `handoff_ssl_options` in `riak_core`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_core/src/riak_core_handoff_sender.erl](https://github.com/OpenRiak/riak_core/blob/2903cdc194fa4d538dd6f6da359e8465c11bb3c2/src/riak_core_handoff_sender.erl#L675)

# Reviewed against

3.4.0: 934adc29bab17c3716e2a9a20f1e86d37800ff5fa1ebc3c39f1d4a0677aa1fa0
3.4.1: 934adc29bab17c3716e2a9a20f1e86d37800ff5fa1ebc3c39f1d4a0677aa1fa0
