# Metadata

command: erlang:riak:join/1
versions: 3.4.0, 3.4.1

# Summary

Join another node through the legacy Erlang API.

# Description

Directly calls riak_core:join/1. Prefer staged cluster join/plan/commit for a reviewed operational change.

# Arguments

## Node

datatype: Erlang node atom
required: true
repeatable: false

### Description

See the shared `Node` argument on the parent module page.

# Results

## reference-result-1

### Description

A valid request joins the node through the legacy API; verify membership and convergence afterward.

# Examples

## erlang-riak-join:join-reachable-node

title: Join a reachable node

### Description

Join the second node and inspect the resulting ring members. This legacy API changes membership directly; prefer the staged CLI workflow for planned cluster changes.

# Reviewed against

3.4.0: 97aadf8f1d81bffad665e0bb7bc29d715219b9a130b2788faf10182bef298830
3.4.1: 97aadf8f1d81bffad665e0bb7bc29d715219b9a130b2788faf10182bef298830
