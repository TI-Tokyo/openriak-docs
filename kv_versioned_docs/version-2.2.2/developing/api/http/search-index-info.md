---
title: "HTTP Search Index Info"
sidebar_position: 114
sidebar_label: Search Index Info
pagination_label: "HTTP Search Index Info"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2017-03-24
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Retrieves information about all currently available [Search indexes](./../../../usage/search) in JSON format.

## Request

```
GET /search/index
```

## Response

If there are no currently available Search indexes, a `200 OK` will be
returned but with an empty list as the response value.

Below is the example output if there is one Search index, called
`test_index`, currently available:

```json
[
  {
    "n_val": 3,
    "name": "test_index",
    "schema": "_yz_default"
  }
]
```

#### Normal Response Codes

* `200 OK`

#### Typical Error Codes

* `404 Object Not Found` --- Typically returned if Riak Search is not
    currently enabled on the node
* `503 Service Unavailable` --- The request timed out internally
