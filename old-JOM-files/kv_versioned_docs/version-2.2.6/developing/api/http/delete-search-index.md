---
title: "HTTP Delete Search Index"
sidebar_position: 116
sidebar_label: Delete Search Index
pagination_label: "HTTP Delete Search Index"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2018-05-22
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Deletes a Riak Search index.

## Request

```
DELETE /search/index/<index_name>
```

## Normal Response Codes

* `204 No Content` --- The index was successfully deleted (also returned
    if the index did not exist to begin with)

## Typical Error Codes

* `503 Service Unavailable` --- The request timed out internally
