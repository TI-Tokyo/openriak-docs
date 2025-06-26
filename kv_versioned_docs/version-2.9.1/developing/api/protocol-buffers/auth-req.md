---
title: "PBC Auth Request"
sidebar_position: 125
sidebar_label: Auth Request
pagination_label: "PBC Auth Request"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2020-02-16
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


Sends a username (`user`) and password (`password`) to Riak as part of
an authentication request. Both values are sent as binaries.

## Request

```protobuf
message RpbAuthReq {
    required bytes user = 1;
    required bytes password = 2;
}
```

For more on authentication, see our documentation on [Authentication and Authorization](./../../../../using/security/basics).
