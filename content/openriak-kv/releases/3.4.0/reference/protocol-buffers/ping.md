---
title: 'Ping with Protocol Buffers'
description: 'Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.'
weight: 13
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\api\protocol-buffers\ping.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Document the Protocol Buffers contract for this operation, including messages, fields, streaming behavior, examples, and errors.

## Details

### PBC Ping

Check if the server is alive

#### Request

Just the `RpbPingReq` message code. No request message defined.

#### Response

Just the `RpbPingResp` message code. No response message defined.

#### Example

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
