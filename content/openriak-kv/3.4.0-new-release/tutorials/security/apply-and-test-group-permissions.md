---
title: Apply and test group permissions
weight: 380
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Verify that group membership grants a read but not a write, then revoke the grant. Continue directly
  from the authenticated TLS lesson.
related:
- tutorials/security/make-an-authenticated-tls-client-connection
- tutorials/security/rotate-a-certificate-in-a-learning-environment
- how-to/security/manage-groups-and-membership
- how-to/security/grant-and-revoke-permissions
- reference/commands/riak/admin/security
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: tutorials/security/make-an-authenticated-tls-client-connection
next_page: tutorials/security/rotate-a-certificate-in-a-learning-environment
---

Verify that group membership grants a read but not a write, then revoke the grant. Continue directly from the authenticated TLS lesson.

## Test the existing reader

```sh
curl --fail --cacert tls/ca.crt --user docs-reader:docs-learning-password   https://127.0.0.1:18099/buckets/client-demo/keys/secure
curl -i --cacert tls/ca.crt --user docs-reader:docs-learning-password   -X PUT -H 'Content-Type: text/plain' --data-binary 'not allowed'   https://127.0.0.1:18099/buckets/client-demo/keys/secure
```

The read succeeds and the write is rejected. The second command intentionally leaves the error response visible. Check that the object still contains `TLS works`.

## Inspect and revoke

{{< cli-example key="shell:riak admin security print-grants" prefix="kv node1" args="docs-reader" >}}

{{< cli-example key="shell:riak admin security revoke" prefix="kv node1" args="riak_kv.get on default client-demo from docs-readers" >}}

Repeat the read using a new curl request. It should now be denied. If it still succeeds, inspect direct user grants and other group memberships.

## Restore the lesson state

Grant the same read permission back to `docs-readers`, using the grant operation from the preceding lesson. Confirm a successful read before continuing to certificate rotation. This restores only the exercise's permission, not general write access.
