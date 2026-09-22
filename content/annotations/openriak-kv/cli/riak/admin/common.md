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

# Options

## -sort

omit: true



## -lines

omit: true



## -interval

omit: true

# Results

## outcome

### Description

Dispatches the selected administrative command. Read the child command’s results and errors; an RPC connection or cookie failure prevents dispatch.

# Reviewed against

3.4.0: eb83ddd2adac68ac523a0d4c8ab972d3f9eced34f6dc8d313ff78497bef0a32b
3.4.1: 871340f907cb28cb28460f40be2789ff5f487f029a85f0a6532ed076891b37aa
