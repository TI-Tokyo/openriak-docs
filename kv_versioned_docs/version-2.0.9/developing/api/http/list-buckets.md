---
title: "HTTP List Buckets"
sidebar_position: 103
sidebar_label: List Buckets
pagination_label: "HTTP List Buckets"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2017-03-15
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Lists all known buckets (ones that have keys stored in them).

<RiakDocsNote title="Not for production use">
Similar to the list keys operation, this requires traversing all keys stored
in the cluster and should not be used in production.
</RiakDocsNote>

## Request

```bash
# Using the default bucket type
GET /buckets?buckets=true

# Using a non-default bucket type
GET /types/<type>/buckets?buckets=true
```

Required query parameter:

* **buckets=true** - required to invoke the list-buckets functionality

## Response

Normal status codes:

* `200 OK`

Important headers:

* `Content-Type - application/json`

The JSON object in the response will contain a single entry, "buckets", which
will be an array of bucket names.

## Example

```curl
$ curl -i http://localhost:8098/buckets?buckets=true
HTTP/1.1 200 OK
Vary: Accept-Encoding
Server: MochiWeb/1.1 WebMachine/1.9.0 (participate in the frantic)
Date: Fri, 30 Sep 2011 15:24:35 GMT
Content-Type: application/json
Content-Length: 21

{"buckets":["files"]}
```
