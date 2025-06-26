---
title: "Riak KV 2.9.7 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 2.9.7 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2020-08-16
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Aug 16, 2020.

## Overview

This release improves the stability of Riak when running with Tictac AAE in parallel mode:

- The aae_exchange schedule will back-off when exchanges begin to timeout due to pressure in the system.

- The aae_runner now has a size-limited queue of snapshots for handling exchange fetch_clock queries.

- The aae tree rebuilds now take a snapshot at the point the rebuild is de-queued for work, not at the point the rebuild is added to the queue.

- The loading process will yield when applying the backlog of changes to allow for other messages to interleave (that may otherwise timeout).

- The aae sub-system will listen to back-pressure signals from the aae_keystore, and ripple a response to slow-down upstream services (and ultimately the riak_kv_vnode).

- It is possible to accelerate and decelerate AAE repairs by setting riak_kv application variables during running (e.g tictacaae_exchangetick, tictacaae_maxresults), and also log AAE-prompted repairs using log_readrepair.

The system is now stable under specific load tests designed to trigger AAE failure. However, parallel mode should still not be used in production systems unless it has been subject to environment-specific load testing.

[Previous Release Notes](#previous-release-notes)

## Previous Release Notes

Please see the KV 2.9.4 release notes [here](./../../2.9.2/release-notes), the KV 2.9.2 release notes [here](./../../2.9.1/release-notes), and the KV 2.9.1 release notes [here](./).

