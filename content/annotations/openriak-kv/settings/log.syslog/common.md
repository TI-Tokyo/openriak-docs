# Description

Legacy `log.syslog` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.additional_handlers` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: de8a30ed7af62f781bc8163cfa9adfcfcab082e1546f60b36eb89adb8acd511f
3.4.1: de8a30ed7af62f781bc8163cfa9adfcfcab082e1546f60b36eb89adb8acd511f
