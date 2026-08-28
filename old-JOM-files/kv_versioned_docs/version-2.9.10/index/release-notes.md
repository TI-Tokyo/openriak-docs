---
title: "Riak KV 2.9.10 Release Notes"
sidebar_position: 101
sidebar_label: Release Notes
pagination_label: "Riak KV 2.9.10 Release Notes"
hide_table_of_contents: true
slug: /release-notes
last_update:
  author: RiakDocs
  date: 2021-10-06
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Released Oct 06, 2021.

## Overview

Fix to critical issue in leveled when using (non-default, but recommended, option): [leveled_reload_recalc = enabled](https://github.com/basho/riak_kv/blob/33add2a29b6880b680a407dc91828736f54c7911/priv/riak_kv.schema#L1156-L1174)

If using this option, it is recommended to rebuild the ledger on each vnode at some stage after updating.

## Previous Release Notes

Please see the KV 2.9.9 release notes [here](./../../2.9.9/release-notes).

