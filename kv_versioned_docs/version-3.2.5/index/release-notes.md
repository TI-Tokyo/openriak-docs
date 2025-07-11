---
title: "Riak KV 3.2.5 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.2.5 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2025-03-24
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released March 25, 2025.

## Overview

This release contains the following fixes and enhancements:

This release contains a fix for the nextgen replication full-sync solution, fixing an issue for which there already exists a workaround in Riak 3.2.4. Unless clusters have very high key counts (i.e. around 10 billion objects are larger), the workaround in Riak 3.2.4 should generally be sufficient, and so the update is non-urgent.


## Previous Release Notes

Please see the KV 3.2.4 release notes [here](./../../3.2.4/release-notes).

