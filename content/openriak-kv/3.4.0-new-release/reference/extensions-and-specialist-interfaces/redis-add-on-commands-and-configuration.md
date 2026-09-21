---
title: Redis add-on commands and configuration
weight: 1270
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: The Redis add-on is a separate integration with its own command and cache behaviour. It must be matched
  to an identified add-on build and compatible OpenRiak deployment; a standard OpenRiak package does not by itself
  est
related:
- how-to/legacy-and-specialist-workflows/set-up-a-compatible-redis-add-on-deployment
- how-to/legacy-and-specialist-workflows/use-and-monitor-the-redis-add-on
- how-to/legacy-and-specialist-workflows/develop-an-application-using-the-redis-add-on
- reference/orientation-and-compatibility/feature-status-and-deprecations
- foundations/storage-and-performance/storage-backend-trade-offs
---

The Redis add-on is a separate integration with its own command and cache behaviour. It must be matched to an identified add-on build and compatible OpenRiak deployment; a standard OpenRiak package does not by itself establish that the add-on is installed.

## Integration contract

Check which Redis commands the add-on implements, how it maps keys and values into backing objects, when changes are written through, and what happens when cached and stored data disagree. Compatibility with a subset of Redis operations is not compatibility with every Redis client workflow.

## Operational boundaries

The add-on's listener, credentials, cache memory, expiry, and persistence behaviour are separate from the backing cluster's object policy. Restarting or losing a cache process must be evaluated against the intended source of truth.

Use the specialist setup and application guides only with their matching component source and version. Do not infer a currently verified package or a complete Redis command catalogue from the historical examples.
