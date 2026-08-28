---
title: "Riak KV 3.0.12 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.12 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2022-12-20
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Dec 20, 2022.

## Overview

This is a general release of changes and fixes:

* A fix to a critical issue with the use of PR variables in Riak KV (when the PR value is set via bucket properties).

*  Changes to the leveled backend with the aim of further improving memory management, by simplifying the summary tree within each leveled_sst file.

* An update to leveldb snappy compression, to make Riak compatible with a broader set of platforms (including AWS Graviton). Because of this change, anyone building from source will now require cmake to be installed.

* A new `reip_manual` console command has been added to use as an alternative to reip, which does not currently work in the 3.0 release stream. Use `riak admin reip_manual` in place of riak admin reip when performing the reip operation on a node. This now requires that the path to the ring file, and the cluster name, to be known by the operator.

* Some improvements to logging within the leveled backend have been made to allow for better statistics monitoring of low-level operations, and reduce the cost of writing a log within leveled.

* A fix for a deadlock issue in riak_repl AAE fullsync to help when clusters with high object counts have large deltas.

* Two other fixes within Riak KV.

* As part of this release, further testing of the new memory configuration options added in Riak 3.0.10 has been undertaken. It is now recommended when using the leveled backend, that if memory growth in the Riak process is a signifcant concern, then the following configuration option may be tested: erlang.eheap_memory.sbct = 128. This has been shown to reduce the memory footprint of Riak, with a small performance overhead.

## Previous Release Notes

Please see the KV 3.0.11 release notes [here](./../../3.0.11/release-notes).

