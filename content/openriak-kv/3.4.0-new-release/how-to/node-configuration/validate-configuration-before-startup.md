---
title: Validate configuration before startup
description: Validate the intended configuration before starting or restarting a node. Run the check with the same
  installation, environment, and file paths used by the service.
weight: 250
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---key-riakconf-changes
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/verify-configuration.md
related:
- how-to/node-configuration/inspect-and-manage-effective-configuration
- how-to/installation/verify-an-installation
- how-to/troubleshooting/diagnose-a-node-that-will-not-start
- reference/configuration/configuration-files-syntax-and-precedence
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
- foundations/cluster-architecture/the-lifecycle-of-a-read-and-a-write
previous_page: how-to/node-configuration/configure-http-and-protocol-buffers-listeners
next_page: how-to/installation/verify-an-installation
---

Validate the intended configuration before starting or restarting a node. Run the check with the same installation, environment, and file paths used by the service.

## Check files and permissions

Save the current configuration. Check that referenced data directories, certificate files, and log directories exist and are accessible to the service account. Confirm that listener ports are available and the node's hostname resolves correctly.

## Run the validator

{{< cli-example key="shell:riak chkconfig" >}}

Correct each reported unknown key, invalid value, or Erlang syntax error, then rerun the check. Use [All configuration settings and defaults]({{< product-version-root >}}reference/configuration/all-configuration-settings-and-defaults/) for allowed values and platform defaults. Do not suppress validation errors by deleting unrelated settings.

## Inspect the proposed effective configuration

Review generated application terms and VM arguments for unintended changes, especially identity, backend, ring size, listeners, and security. Validation checks translation and syntax; it does not prove that peers are reachable or that credentials work.

## Start and verify

Restart according to [Start, stop, or restart a node]({{< product-version-root >}}how-to/cluster-lifecycle/start-stop-or-restart-a-node/) or [Perform a rolling restart]({{< product-version-root >}}how-to/cluster-lifecycle/perform-a-rolling-restart/), then inspect logs and perform a read/write check through the real client path. Keep the saved configuration available for a controlled rollback.
