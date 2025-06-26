---
title: "Riak KV 3.0.3 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 3.0.3 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2021-01-14
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Jan 14, 2021.

## Overview

There are two fixes provided in Release 3.0.3:

* A performance issue with OTP 22 and leveled has been corrected. This generally did not have a significant impact when running Riak, but there were some potential cases with Tictac AAE and AAE Folds where there could have been a noticeable slowdown.

* An issue with console commands for bucket types has now been fully corrected, having been partially mitigated in 3.0.2.

This release is tested with OTP 20, OTP 21 and OTP 22; but optimal performance is likely to be achieved when using OTP 22.

## Previous Release Notes

Please see the KV 3.0.2 release notes [here](./../../3.0.2/release-notes).

