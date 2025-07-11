---
title: "Riak KV 3.0.14 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.14 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2023-02-13
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Feb 13, 2023.

## Overview

This release fixes an issue whereby a failure to signal and handle back-pressure correctly by the leveled backend can cause a backlog within the store. In particular this can be triggered by handoffs (e.g. due to cluster admin operations), and lead to partition transfers stalling almost completely. The issue existed in previous releases, by may have been exacerbated by refactoring in Riak KV 3.0.13.

An additional minor improvement has been made to handoffs. Previously requests to reap tombstones after deletions (where the `delete_mode` is not keep), would not be forwarded during handoffs. These tombstones would then need to be corrected by AAE (which may result in a permanent tombstone). There is now a configuration option `handoff_deletes` which can be enabled to ensure these reap requests are forwarded, reducing the AAE work required on handoff completion.

Desipite the handoff improvements in Riak KV 3.0.13, handoff timeouts are still possible. If handoff timeouts do occur, then the first stage should be to reduce the handoff batch threshold count to a lower number than that of the item_count in the handoff sender log.

## Previous Release Notes

Please see the KV 3.0.13 release notes [here](./../../3.0.13/release-notes).

