---
title: "Riak KV 2.9.1 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 2.9.1 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2020-02-16
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Feb 15, 2020.

## Overview

This release adds a number of features built on top of the Tictac AAE feature made available in 2.9.0. The new features depend on Tictac AAE being enabled, but are backend independent. The primary features of the release are:

* A new combined full-sync and real-time replication system nextgenrepl, that is much faster and more efficient at reconciling overall state of clusters (e.g. full-sync).

* A mechanism for requesting mass deletion of objects on expiry, and mass reaping of tombstones after a time to live. This is not yet an automated, scheduled, set of garbage collection processes, it is required to be triggered by an operational process.

* A safe method of listing buckets regardless of backend chosen. Listing buckets had previously not been production safe, but can still be required in production environments - it can now be managed safely via an `aae_fold`.

* A version uplift of the internal ibrowse client, a minor riak_dt fix to resolve issues of unit test reliability, a fix to help build (the now deprecated) erlang_js in some environments, and the removal of hamcrest as a dependency.

[Previous Release Notes](#previous-release-notes)

## Previous Release Notes

Please see the KV 2.9.0p5 release notes [here](./../2.9.0p5/release-notes), and the KV 2.2.6 release notes [here](./../../2.2.6/release-notes).
