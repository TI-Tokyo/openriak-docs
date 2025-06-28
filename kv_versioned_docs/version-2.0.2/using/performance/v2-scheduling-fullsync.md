---
title: "V2 Scheduling Fullsync"
sidebar_position: 103
sidebar_label: V2 Scheduling Fullsync
pagination_label: "V2 Scheduling Fullsync"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2014-10-18
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


With the `pause` and `resume` commands it is possible to limit the
fullsync operation to off-peak times. First, disable `fullsync_interval`
and set `fullsync_on_connect` to `false`. Then, using cron or something
similar, execute the commands below at the start of the sync window.
In these examples, the commands are combined in a `.sh` or analogous
file:

```bash
#!/bin/sh

## Resume from where we left off

riak-repl resume-fullsync

## Start fullsync if nothing is running

riak-repl start-fullsync
```

At the end of the sync window:

```bash
#!/bin/sh

## Stop fullsync until start of next sync window

riak-repl pause-fullsync
```
