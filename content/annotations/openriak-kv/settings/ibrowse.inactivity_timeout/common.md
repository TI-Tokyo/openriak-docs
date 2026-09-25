# Description

Idle timeout, in milliseconds, for an ibrowse HTTP connection with no current request. The ibrowse configuration table takes precedence over this application value; active requests use their own `inactivity_timeout` option.

# Datatype

Integer

# Units

- milliseconds

# Constraints

- The application value must be an integer greater than zero; other values fall back to `10000`.

# Inferred default

`10000` when the application value is absent or invalid; an integer in the ibrowse configuration table takes precedence.

# Tags

feature: client-networking
repository: ibrowse
module: ibrowse_http_client
concept: connections

# Notes

This is the Erlang application environment key `inactivity_timeout` in `ibrowse`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [ibrowse/src/ibrowse_http_client.erl](https://github.com/OpenRiak/ibrowse/blob/3fd17dd33c474800a4d02ad4e5ae9d4db45e0335/src/ibrowse_http_client.erl#L2122)

# Reviewed against

3.4.0: 1298744c01e0d133c120b1235a7cf925d5e4e9f2c30526e6430c908623a0cb18
3.4.1: 1298744c01e0d133c120b1235a7cf925d5e4e9f2c30526e6430c908623a0cb18
