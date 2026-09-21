---
title: Tune a deployment on AWS
description: Tune an AWS deployment from measured instance, storage, and network behaviour. Keep a stable production
  workload and recovery target when comparing infrastructure choices.
weight: 1220
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- performance-engineers
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\amazon-web-services.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/tune/tune-aws-deployment.md
related:
- tutorials/first-cluster/cloud/aws-ec2
- how-to/planning-a-deployment/size-a-cluster-and-reserve-recovery-headroom
- how-to/cluster-lifecycle/replace-nodes-without-stopping-the-cluster
- how-to/performance/benchmark-a-representative-workload
- how-to/performance/tune-filesystems-memory-and-network-settings
- foundations/storage-and-performance/latency-queues-and-resource-contention
- foundations/storage-and-performance/capacity-and-growth
---

Tune an AWS deployment from measured instance, storage, and network behaviour. Keep a stable production workload and recovery target when comparing infrastructure choices.

## Identify the limiting resource

Compare Riak latency and queue growth with EC2 CPU, network, and EBS latency/throughput observations. Check whether the instance or volume is reaching its provisioned or burst limits. Include cross-zone traffic and recovery transfers in the measurement.

## Test a specific change

Benchmark the same dataset on candidate instance and volume configurations. Evaluate sustained behaviour after burst capacity is exhausted. Preserve node identity and data during infrastructure changes, and use a planned replacement when moving storage or instance families.

## Verify resilience and cost

Rehearse one unavailable member and a rolling replacement. Confirm that the surviving deployment meets application latency and recovery targets. Review retained EBS backups, transfer charges, and unused resources along with compute cost; compare measured total capacity rather than a nominal instance specification.

Use current AWS instance and EBS documentation for the selected Region's supported combinations and limits. For a disposable first deployment, follow [Build a learning cluster on AWS EC2]({{< product-version-root >}}tutorials/first-cluster/cloud/aws-ec2/).
