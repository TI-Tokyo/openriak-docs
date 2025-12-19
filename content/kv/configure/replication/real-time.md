---
title: real-time sync
sidebar_label: "real-time sync"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[overview]: #overview
[enable realtime]: #enable-realtime
[queues]: #queues

Other pages in this section:

1. [Queues](: ../../configure/replication/queue)
2. [sink](: ../../configure/replication/queue)
3. [fullsync](: ../../configure/replication/fullsync)

NextGenRepl’s RealTime feature provides a considerable improvement over the legacy realtime engines of Riak. It is faster, more efficient, and more reliable. NextGenRepl is the recommended replication engine to use with OpenRiak.

RealTime will ensure that the data in the sink cluster is updated as quickly as possible from the source clusters.

---

NextGenRepl relies on [TicTac-AAE](: ../../configure/replication/) , so this must be enabled.

---

## Overview

As changes occur on the source cluster, NextGenRepl’s RealTime replication system will add them to one or more configurable queues within the replication queuing system.

A source node can be the source for multiple sink clusters by using multiple queues.

---

As of writing, all changes listed in this documentation to NextGenRepl must be made by changing the values in the `riak.conf` file.

---

## Enable RealTime

RealTime changes are added to the queuing system by setting:

```bash
replrtq_enablesrc = enabled
```

By default, RealTime is turned off (`disabled`).

## Queues

At least one replication queue should allow RealTime objects to be added. The easiest way to do this is to have a queue filter of any, but other options are available, see the page on [queues](: ../..//configure/replication/queue).

By default, there is no queue setup for RealTime. To set the default queue to also allow RealTime queues, change the following:

```bash
replrtq_srcqueue = q1_ttaaefs:block_rtq
```

to 

```bash
replrtq_srcqueue = q1_ttaaefs:any
```

To add a new queue called `my-replication-queue` that allowed RealTime replication for any bucket, you would add `my-replication-queue:any` to the `replrtq_srcqueue` setting. For example, to keep the default FullSync-only queue and add a second queue for RealTime you would set:

```bash
replrtq_srcqueue = q1_ttaaefs:block_rtq|my-replication-queue:any
```
