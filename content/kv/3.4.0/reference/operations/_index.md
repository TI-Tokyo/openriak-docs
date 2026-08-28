---
title: 'Operations reference'
description: 'Define runtime files, metrics, state, and operational behavior used during cluster administration.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define runtime files, metrics, state, and operational behavior used during cluster administration.

## Details

### OpenRiak KV Usage Reference

[ref log]: ./logging
[ref handoff]: ./handoff
[ref bucket types]: ./bucket-types
[ref obj del]: ./object-deletion/
[ref runtime]: ./runtime-interaction/
[ref monitoring]: ./statistics-monitoring
[ref snmp]: ./snmp
[ref jmx]: ./jmx
[ref 2i]: ./secondary-indexes
[ref custom code]: ./custom-code
[ref strong consistency]: ./strong-consistency
[ref mdc]: ./multi-datacenter
[ref v3 mdc]: ./v3-multi-datacenter
[ref v2 mdc]: ./v2-multi-datacenter
[ref arch]: ./architecture

#### In This Section

##### [Logging Reference][ref log]

Overview of logging in OpenRiak KV.

[Learn More >>][ref log]

###### [Handoff Reference][ref handoff]

Details OpenRiak KV's handoff system.

[Learn More >>][ref handoff]

###### [Bucket Types Reference][ref bucket types]

Explanation of bucket types in OpenRiak KV.

[Learn More >>][ref bucket types]

###### [Object Deletion Reference][ref obj del]

Information on object deletion scenarios and tombstones.

[Learn More >>][ref obj del]

###### [Runtime Interaction Reference][ref runtime]

Describes the how Riak interacts with distribution ports and operating system
processes/garbage collection.

[Learn More >>][ref runtime]

###### [Statistics & Monitoring Reference][ref monitoring]

Presents commonly monitored & gathered statistics, as well as solutions for monitoring and gathering statistics.

[Learn More >>][ref monitoring]

###### [Simple Network Management Protocol][ref snmp]

Cover's Riak Enterprise's deprecated SNMP server used allow an external system to query nodes for statistics.

[Learn More >>][ref snmp]

###### [JMX Monitoring][ref jmx]

Details OpenRiak KV's deprecated JMX monitoring system.

[Learn More >>][ref jmx]

###### [Secondary Indexes Reference][ref 2i]

Implementation details for OpenRiak KV's secondary indexes feature

[Learn More >>][ref 2i]

###### [Installing Custom Code][ref custom code]

Steps for installing custom code modules for pre/post-commit hooks and MapReduce operations.

[Learn More >>][ref custom code]

###### [Strong Consistency Reference][ref strong consistency]

Overview of strong consistency in OpenRiak KV.

[Learn More >>][ref strong consistency]

###### [Multi-Datacenter Reference][ref mdc]

Overview of OpenRiak's Multi-Datacenter system.

[Learn More >>][ref mdc]

###### [V3 Multi-Datacenter Replication Reference][ref v3 mdc]

Details OpenRiak's V3 Multi-Datacenter system.

[Learn More >>][ref v3 mdc]
