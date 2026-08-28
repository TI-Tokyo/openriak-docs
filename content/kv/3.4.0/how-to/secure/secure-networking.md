---
title: 'Harden OpenRiak network access'
description: 'Show security engineers how to harden openriak network access and test the resulting controls.'
weight: 8
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'security-engineers'
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\networking.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/BuildAndScaleClusterGuide.html#network'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show security engineers how to harden openriak network access and test the resulting controls.

## Before you begin

Secure administrative access, an inventory of identities and certificates involved, and a tested rollback path that will not lock operators out.

## Overview

### Network

> As a distributed database, Riak may place significant demands on the underlying network infrastructure.

For the high-level design of networks supporting Riak clusters, consideration is required of the following factors:

- When using Riak to store and retrieve large (e.g. o(100KB) or bigger) objects, network bandwidth may be the bottleneck and in many systems bandwidth of more than 1 Gbps will be required.
- TCP incast is a generic problem in distributed systems, where multiple nodes return the same object to a coordinating node concurrently.
  - Since Riak 3.0, depending on storage backend, the potential for incast issues is significantly mitigated by coordinating with object metadata transmission rather than value transmission.
  - It is still prudent to consider the potential for incast problems in network design - in particular ensuring that network switches are data-centre class with appropriate buffer sizes.
- It is assumed in the design and development of Riak that network round-trip times within a cluster are o(1ms) or better.  At higher latencies network delays will tend to become the most significant proportion of the overall user response delay.
  - There is no assumption of minimal network latency between clusters, so resilience across geographically diverse locations with long round-trip times should be managed by running multiple clusters.

Riak is partition tolerant, in that during partition events data can still be stored securely across multiple nodes, and values can be merged (potentially forming siblings where conflicts cannot be resolved) when partitions heal.  Read events (both Object and Query API calls) may still not succeed correctly during partitions, particularly on minority partitions.

> Regardless of the partition tolerance in the Riak architecture, it is still important to design networks running Riak clusters so that partition events are rare.

If there are weaknesses in resilience in the network architecture, then that resilience should be reflected in the configuration of locations.  For example, if nodes are only connected to a single network switch, then all nodes on the same switch should be configured to be in the same location.

In assessing the bandwidth needs of Riak deployments, the flow of requests using [the Object API](/kv/3.4.0/reference/http-api/) should be considered:

- For every GET from Riak, the value will normally be fetched once within the cluster (the majority of the time from within the same location) generating an intra-cluster network bandwidth requirement.
- For every PUT the value will normally be sent three times within the cluster.  Between replicating clusters GETs do not create network bandwidth needs, but each PUT requires a single transfer of the value.
- The flow of requests may change depending on the choice of both n_val and storage backend.

Riak has the option to enforce compression in the storage backend, but this will not lead to generic enablement of object compression for intra-cluster communication

- The intra-cluster network must support the bandwidth necessary to transmit uncompressed objects within the cluster, and back to clients.
- Compression of objects replicating between clusters may be enabled via configuration.

Riak has the potential to use two different transport protocols - HTTP and PB.  For the security of communication in the environment, consideration is required of the following factors:

- The Riak API uses either protocol buffers (PB) or HTTP, and both interfaces can be converted to require TLS encryption - by configuring an additional listener for HTTPS and by negotiation on the in-clear listener with PB.
  - To ensure full protection from network eavesdropping, TLS enablement must also be enforced in the [Erlang Distribution Protocol](https://www.erlang.org/doc/apps/ssl/ssl_distribution.html).  TLS enablement must also be separately configured in the `riak.conf` file to ensure protection of handoff communication, and of replicated traffic.
  - Access controls with TLS enablement can be made via certificate or username/password identification with the PB API, but it is only tested with username/password authentication via the HTTPS API.
- It is common for Riak users to enforce network protection within the infrastructure, rather than within the database itself, for example through use of the AWS nitro system.

> A proxy for an OpenRiak cluster will generally require a significant amount of bandwidth, especially where the cluster is supporting relatively large objects.  Scaling proxy bandwidth may require a step-change in underlying network technology compared to that of the individual nodes.

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## Verify the result

Test permitted and denied access separately, validate certificate and identity details, and review security-related logs.
