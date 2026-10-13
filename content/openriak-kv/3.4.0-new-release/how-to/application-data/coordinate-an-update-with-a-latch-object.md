---
title: Coordinate an update with a latch object
weight: 460
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: Reviewed
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-27'
review_scope: content review
review-by: TI Tokyo/JOM
description: Use a conditionally created object as an application marker for a bounded activity, such as claiming
  a batch. Define how ownership and interrupted work are recovered before introducing the marker.
related:
- reference/http-api/conditional-requests-and-latch-objects
- how-to/application-data/make-conditional-reads-and-writes
- foundations/data-and-consistency/conditional-updates-and-latch-objects
features: ["client-operations","conditional-writes"]
concepts: ["concurrency-control","data-access"]
---

Use a small, purpose‑built object to mark when a specific task is in progress-like claiming a batch. Before you create that marker, spell out how ownership will be assigned and how any stopped or unfinished work will be recovered.

## Establish the contract

Pick a single key to represent each claim, and store both the owner and the work identifier in its value. Every writer that participates in the workflow must follow the same conditional‑update rules. Remember that a latch only protects the key it’s attached to—other keys are not updated atomically—so review the boundaries of conditional updates before depending on it.

## Create the claim

When using the HTTP object endpoint, send the creation request with `If-None-Match: *.` Include deliberate application data in the body. If the request fails its precondition, it means another value already holds the claim; treat this as a signal to stop, not as permission to overwrite the existing value.

## Complete or recover the work

Read the marker, keep its causal context, and confirm that the owner matches before moving the work forward. Make downstream steps safe to retry by using the work identifier. Because timeouts can leave a valid claim behind, always inspect the marker before attempting a retry.

## Verify contention scenario

Test how the system behaves when two workers try to claim the same identifier, when a worker stops immediately after claiming, and when a retry happens after an uncertain response. Ensure your recovery logic avoids repeating non‑idempotent actions and doesn’t leave any work permanently unclaimable. Preserve sibling‑handling logic for rare or exceptional concurrency cases.
