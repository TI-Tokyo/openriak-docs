---
title: "Riak KV 3.0.6 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.6 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2021-05-07
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released May 10, 2021.

## Overview

Release 3.0.6 adds location-awareness to Riak cluster management. The broad aim is to improve data diversity across locations (e.g. racks) to reduce the probability of data-loss should a set of nodes fail concurrently within a location. The location-awareness does not provide firm guarantees of data diversity that will always be maintained across all cluster changes - but testing has indicated it will generally find a cluster arrangement which is close to optimal in terms of data protection.

If location information is not added to the cluster, there will be no change in behaviour from previous releases.

There may be some performance advantages when using the location-awareness feature in conjunction with the leveled backend when handling GET requests. With location awareness, when responding to a GET request, a cluster is more likely to be able to fetch an object from a vnode within the location that received the GET request, without having to fetch that object from another location (only HEAD request/response will commonly travel between locations).

This release is tested with OTP 20 and OTP 22; but optimal performance is likely to be achieved when using OTP 22.

## Previous Release Notes

Please see the KV 3.0.4 release notes [here](./../../3.0.4/release-notes).

