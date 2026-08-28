---
title: "PBC Ping"
sidebar_position: 110
sidebar_label: Ping
pagination_label: "PBC Ping"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2024-12-09
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Check if the server is alive

## Request

Just the `RpbPingReq` message code. No request message defined.

## Response

Just the `RpbPingResp` message code. No response message defined.

## Example

Request

```bash
Hex    00 00 00 01 01
Erlang <<0,0,0,1,1>>
```

Response

```bash
Hex    00 00 00 01 02
Erlang <<0,0,0,1,2>>
```

