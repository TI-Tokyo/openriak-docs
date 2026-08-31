---
title: "Riak KV 3.0.11 Release Notes"
description: ""
project: "riak_kv"
project_version: "3.0.11"
lastmod: 2022-10-12T00:00:00-00:00
sitemap:
  priority: 0.2
menu:
  riak_kv-3.0.11:
    name: "Release Notes"
    identifier: "index_release_notes"
    weight: 101
    parent: index
toc: false
aliases:
  - /riak/3.0.11/community/release-notes
  - /openriak-kv/3.0.11/intro-v20
  - /riak/3.0.11/intro-v20
  - /openriak-kv/3.0.11/introduction
linkTitle: "Release Notes"
weight: 101
---

Released Oct 11, 2022.

## Overview

A simple change to release a bottleneck in 2i queries with the leveled backend. Should only be relevant to those using leveled, and attempting o(1000) 2i queries per second.

## Previous Release Notes

Please see the KV 3.0.8 release notes [here]({{<baseurl>}}openriak-kv/3.0.10/release-notes/).

