# Summary

Run administrative commands against an OpenRiak KV node.

# Description

Choose a subcommand to inspect or change the node and cluster. Subcommands
share the connection to the running node and its Erlang distribution cookie.

# Notes

Run administrative commands with the intended node’s configuration and cookie.
A failure to connect can prevent the subcommand from running at all.

# Examples

## admin:wrong-cookie

title: Incorrect Erlang cookie

### Description

This deliberately uses the wrong cookie with `member-status`. The connection
fails before the membership query runs. Other `riak admin` subcommands use
the same connection check.

# Errors

## admin:wrong-cookie

### Condition

The CLI uses a different Erlang distribution cookie from the target node.

### Description

The launcher reports that the node is not responding to pings and exits with
status `1`. The same message can also occur when the node is stopped or cannot
be reached; it does not identify a cookie mismatch by itself.

### Remedy

Check that the intended node is running and reachable, then use its configured
cookie. Do not change the node’s cookie simply to match this test example.

# Reviewed against

3.4.0: 5ea5255deef13a26dbf89fc655d56c1b43267d911b375ace3db10079ff873b0a
3.4.1: 79aab996a841c4b5e3b6ed172db5cd5ee90268fcc28e8ea99b5bcde61cb95074
