---
title: Coordinate an update with a latch object
weight: 460
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Use a conditionally created object as an application marker for a bounded activity, such as claiming
  a batch. Define how ownership and interrupted work are recovered before introducing the marker.
related:
- reference/http-api/conditional-requests-and-latch-objects
- how-to/application-data/make-conditional-reads-and-writes
- foundations/data-and-consistency/conditional-updates-and-latch-objects
---

Use a conditionally created object as an application marker for a bounded activity, such as claiming a batch. Define how ownership and interrupted work are recovered before introducing the marker.

## Establish the contract

Choose one key per claim and record the owner and work identifier in its value. All cooperating writers must use the conditional protocol. A latch does not make changes to other keys atomic; read the conditional-update boundaries before relying on it.

## Create the claim

For the HTTP object endpoint, make the creation request with `If-None-Match: *`. Use deliberate application values in the body. A failed precondition means another value already prevents this claim; it is not permission to overwrite that value unconditionally.

## Complete or recover work

Read the marker, retain its causal context, and verify the owner before advancing the work state. Make downstream actions safe to retry using the work identifier. A timeout may leave an accepted claim, so inspect the marker before retrying.

## Verify contention

Test two workers claiming the same identifier, a worker stopping after the claim, and a retry after an uncertain response. Confirm that recovery does not run the same non-idempotent action twice or leave work permanently unclaimable. Retain sibling handling for exceptional concurrency.
