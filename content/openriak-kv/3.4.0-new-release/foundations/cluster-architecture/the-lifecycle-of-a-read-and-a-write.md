---
title: The lifecycle of a read and a write
weight: 50
product: OpenRiak KV
product_version: 3.4.0
diataxis: explanation
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: A client can send an object request to a reachable OpenRiak node. That node coordinates work with the
  vnodes responsible for the object's replicas; it need not own the object's primary partition.
related:
- foundations/data-and-consistency/quorums-availability-and-durability
- foundations/data-and-consistency/causality-version-vectors-and-siblings
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- reference/http-api/fetch-object
- reference/http-api/store-object
---

A client can send an object request to a reachable OpenRiak node. That node coordinates work with the vnodes responsible for the object's replicas; it need not own the object's primary partition.

## A write

The coordinator interprets the namespace, bucket policy, causal context, and request options. It sends work to the relevant replicas and waits for the acknowledgements requested by the client. When those conditions are met, it can return success while other work is still in progress.

A timeout means the client did not receive the required success within the time limit. It does not prove that no replica accepted the write. Retrying without preserving the application's identity and update context can create duplicate work or conflicting values.

## A read

The coordinator requests replica responses, reconciles the versions it receives, and returns a value, siblings, a missing-object response, or an error. The result depends on the policy and the responses available for that request. Read repair can update replicas found to be stale.

## Example: a slow replica

If enough replicas acknowledge a write while another is slow, the client may receive success before every copy is updated. A later request can encounter the difference. Read repair and anti-entropy help replicas converge; application conflict handling deals with changes that are concurrent rather than merely late.
