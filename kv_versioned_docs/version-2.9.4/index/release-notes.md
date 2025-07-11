---
title: "Riak KV 2.9.4 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 2.9.4 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2020-07-03
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Jul 03, 2020.

## Overview

This release replaces the Riak KV 2.9.3 release, extending the issue resolution in kv_index_tictactree to detect other files where file truncation means the CRC is not present.

This release has a key outstanding issue when Tictac AAE is used in parallel mode. On larger clusters, this has been seen to cause significant issues, and so this feature should not be used other than in native mode.

TicTac AAE has some useful new functions. [Learn More >>](../using/cluster-operations/tictac-aae-fold).

[Previous Release Notes](#previous-release-notes)

## Previous Release Notes

Please see the KV 2.9.2 release notes [here](./../../2.9.2/release-notes), the KV 2.9.1 release notes [here](./../../2.9.1/release-notes), and the KV 2.9.0p5 release notes [here](./).

