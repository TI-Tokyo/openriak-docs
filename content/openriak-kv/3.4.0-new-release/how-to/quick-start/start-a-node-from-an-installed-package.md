---
title: Start a node from an installed package
weight: 30
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Start a node after installing the release-matched native package. Complete the platform installation
  guide first and keep the client listeners restricted until the node has been verified.
related:
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/node-configuration/configure-http-and-protocol-buffers-listeners
- how-to/cluster-lifecycle/start-stop-or-restart-a-node
- how-to/installation/verify-an-installation
- reference/configuration/node-identity-directories-and-ring-settings
- reference/configuration/listeners-and-networking-settings
---

Start a node after installing the release-matched native package. Complete the platform installation guide first and keep the client listeners restricted until the node has been verified.

## Configure the node

Set its node identity, distribution cookie, data directories, backend, and listeners using the configuration reference. All members of a new cluster need compatible ring and placement choices; each node needs its own identity and local data paths.

## Validate and start

Run the package's configuration check:

{{< cli-example key="shell:riak chkconfig" >}}

Use the service command shown for the operating system and service manager in the node-start reference. If no service manager owns this deployment, use the documented direct launcher. Avoid starting a second process over an already running service.

## Verify

{{< cli-example key="shell:riak ping" >}}

Check the HTTP ping endpoint at the configured listener, then perform a write and read in a test bucket. Inspect logs for backend, identity, and listener errors before joining another node.

If validation fails, correct the reported setting and repeat the check. If the process starts but clients cannot connect, compare the listener binding, firewall, protocol, and client address.
