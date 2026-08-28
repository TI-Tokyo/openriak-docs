---
title: "Riak KV 3.0.4 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.4 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2021-03-24
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released April 2nd, 2021.

## Overview

There are two fixes provided in Release 3.0.4:

* An issue with leveled application dependencies has been resolved, and so lz4 can now again be used as the compression method.

* The riak clients are now compatible with systems that require semantic versioning.

This release is tested with OTP 20, OTP 21 and OTP 22; but optimal performance is likely to be achieved when using OTP 22.

## Previous Release Notes

Please see the KV 3.0.3 release notes [here](./../../3.0.3/release-notes).

