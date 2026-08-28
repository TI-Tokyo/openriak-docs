---
title: "Riak KV 3.2.4 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.2.4 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2025-01-26
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Jan 26, 2025.

## Overview

This release contains the following fixes and enhancements:

* Improve the performance of riak admin status requests whether via or console or web. Note that the statistic for sys_monitor_count will no longer produced as part of this change - but it can be checked if required using the riak_kv_util:sys_monitor_count/0 function.
* Fix an issue with the partial merge feature introduced to the leveled backend in Riak 3.2.3, which could cause vnodes to crash and restart.
* Improve the handling of handoff object folds in leveled to prevent handoff crashes due to bugs or inefficiency that could lead to timeouts.
* Although the issue with partial merge is only expected to occur in relatively rare circumstances, it is recommended that installations presently on Riak 3.2.3 and using the leveled backend, should schedule an upgrade to 3.2.4 as soon as possible.


## Previous Release Notes

Please see the KV 3.2.3 release notes [here](./../../3.2.3/release-notes).

