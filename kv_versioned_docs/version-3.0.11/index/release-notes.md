---
title: "Riak KV 3.0.11 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.11 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2022-10-12
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Oct 11, 2022.

## Overview

A simple change to release a bottleneck in 2i queries with the leveled backend. Should only be relevant to those using leveled, and attempting o(1000) 2i queries per second.

## Previous Release Notes

Please see the KV 3.0.8 release notes [here](./../../3.0.10/release-notes).

