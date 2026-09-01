---
title: 'Configure split and JSON logging'
description: 'Show operators how to route log types to separate handlers and emit structured JSON logs.'
weight: 13
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'content-specification'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to route log types to separate handlers and emit structured JSON logs.

> [!NOTE]
> This page is a content specification. Replace the guidance below with tested OpenRiak KV {{< current-version >}} documentation before publishing it.

## Goal

Define the single practical outcome of **Configure split and JSON logging**, the environments to which it applies, and the supported OpenRiak KV {{< current-version >}} starting state. Keep conceptual background brief and link to an explanation page instead of interrupting the procedure.

## Before you begin

List the required role and permissions, current-state checks, backups or safeguards, tools, configuration files, and maintenance implications. Identify any step that can restart a service, move data, reduce availability, or change compatibility.

## Procedure to write

Add a tested sequence using commands and configuration values copied from OpenRiak KV {{< current-version >}}. For every action, identify where it runs, whether it applies per node or per cluster, what output to expect, and when the operator must wait before continuing.

## Verify the result

Specify independent checks for the intended outcome and overall cluster health. Include the relevant status output, client request, metrics, and log messages, together with clear pass and fail criteria.

## Failure handling and rollback

Describe common errors, safe diagnostic steps, and an explicit rollback or recovery path. State what evidence an operator should collect before escalating an unresolved problem.

## Related documentation

Link to the complete configuration or API reference, the explanation of the underlying mechanism, and any prerequisite or follow-on task.

## In this section

- [Extend configuration with advanced.config]({{< product-version-root >}}how-to/configure/advanced-configuration/) — Show operators how to add advanced configuration without obscuring settings managed in riak.conf.
- [Configure API listeners]({{< product-version-root >}}how-to/configure/api-listeners/) — Show operators how to configure api listeners and verify the result.
- [Configure storage backends]({{< product-version-root >}}how-to/configure/backends/) — Introduce backend configuration procedures after the reader has selected a suitable storage engine.
- [Configure basic node settings]({{< product-version-root >}}how-to/configure/basic-node-settings/) — Show operators how to configure basic node settings and verify the result.
- [Configure global object expiration]({{< product-version-root >}}how-to/configure/global-object-expiration/) — Show operators how to configure global object expiration and verify the result.
- [Configure OpenRiak]({{< product-version-root >}}how-to/configure/) — Introduce task-focused configuration procedures and link each setting to authoritative reference material.
- [Configure a load-balancing proxy]({{< product-version-root >}}how-to/configure/load-balancing-proxy/) — Show operators how to configure a load-balancing proxy and verify the result.
- [Configure logging]({{< product-version-root >}}how-to/configure/logging/) — Show operators how to configure logging and verify the result.
- [Inspect and manage configuration]({{< product-version-root >}}how-to/configure/manage-configuration/) — Show operators how to inspect and manage configuration and verify the result.
- [Configure MapReduce]({{< product-version-root >}}how-to/configure/mapreduce/) — Show operators how to configure mapreduce and verify the result.
- [Configure replication]({{< product-version-root >}}how-to/configure/replication/) — Introduce procedures for configuring anti-entropy and replication within and between clusters.
- [Set runtime environment variables]({{< product-version-root >}}how-to/configure/runtime-environment-variables/) — Show operators how to set supported runtime environment variables and verify their effective values.
- [Enable strong consistency]({{< product-version-root >}}how-to/configure/strong-consistency/) — Show operators how to enable strong consistency and verify the result.
- [Verify configuration before startup]({{< product-version-root >}}how-to/configure/verify-configuration/) — Show operators how to verify configuration before startup and verify the result.
