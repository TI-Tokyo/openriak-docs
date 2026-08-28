---
title: "Riak KV 2.1.4 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 2.1.4 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2016-04-07
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


# Riak KV 2.1.4 Release Notes

Released April 11, 2016.

This is a bugfix release providing patches for the [Riak init file](/community/productadvisories/codeinjectioninitfiles/) Product Advisory and the [leveldb segfault](/community/productadvisories/leveldbsegfault/) Product Advisory.

## Upgraded Components

* LevelDB has been updated to version 2.0.17
* node_package has been updated to version 3.0.0. [See the node_package release notes](https://github.com/basho/node_package/blob/develop/RELEASE-NOTES.md)

## Bugs Fixed

* [[Issue #796](https://github.com/basho/riak/issues/796)/[PR #798](https://github.com/basho/riak/pull/798)] riak-debug has been updated to be compatible with Solaris systems.
