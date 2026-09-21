---
title: Error and diagnostic message catalogue
description: 'Diagnostic messages identify a condition and its context; the same low-level error can have different
  causes in a client request, a backend, or a background job. Preserve the full message, node, timestamp, and operation '
weight: 1050
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\errors.md
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/operations/errors-and-messages.md
related:
- how-to/monitoring-and-diagnostics/collect-diagnostic-evidence
- how-to/troubleshooting/diagnose-a-node-that-will-not-start
- how-to/troubleshooting/diagnose-node-crashes
- how-to/troubleshooting/diagnose-client-connection-and-request-failures
- how-to/troubleshooting/diagnose-missing-stale-or-conflicting-data
- reference/operations-and-observability/log-files-and-event-formats
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/cluster-lifecycle/failure-and-recovery
---

Diagnostic messages identify a condition and its context; the same low-level error can have different causes in a client request, a backend, or a background job. Preserve the full message, node, timestamp, and operation before acting.

## Common conditions

{{< configuration-reference-table reference="diagnostic-errors" >}}{{< /configuration-reference-table >}}

## Request errors

Authentication, validation, precondition, and availability failures require different handling. HTTP status and PB error messages are specified by their interface pages. A condition failure is not a reason to blindly retry a stale write, and a timeout is not proof that no replica accepted it.

## Log and crash context

Keep the surrounding stack trace and structured fields such as partition, peer, queue, event reference, and file path. Backend checksum or manifest errors need store-specific recovery; a generic restart can remove useful evidence without fixing the cause. Redact secrets and application values before sharing diagnostics.

This catalogue covers common conditions, not every possible OTP, filesystem, backend, or custom-hook error. Follow the focused diagnosis for the observed symptom.
