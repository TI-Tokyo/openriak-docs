---
title: Rotate a certificate in a learning environment
weight: 390
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Replace the server certificate while retaining the same learning CA, then verify the new certificate
  and the authenticated application request. Complete the first two security lessons before starting.
related:
- tutorials/security/make-an-authenticated-tls-client-connection
- tutorials/security/apply-and-test-group-permissions
- how-to/security/configure-and-rotate-tls-certificates
- reference/configuration/authentication-authorization-and-tls-settings
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
previous_page: tutorials/security/apply-and-test-group-permissions
---

Replace the server certificate while retaining the same learning CA, then verify the new certificate and the authenticated application request. Complete the first two security lessons before starting.

## Issue a replacement

Record the current serial number and create a new key and signing request:

```sh
openssl x509 -in tls/server.crt -noout -serial
openssl req -new -newkey rsa:3072 -nodes   -keyout tls/server-next.key -out tls/server-next.csr -subj '/CN=localhost'
openssl x509 -req -in tls/server-next.csr -CA tls/ca.crt -CAkey tls/ca.key   -CAserial tls/ca.srl -days 2 -extfile tls/server.ext -out tls/server-next.crt
openssl x509 -in tls/server-next.crt -noout -serial
```

The serial numbers should differ. Verify the new chain with `openssl verify -CAfile tls/ca.crt tls/server-next.crt` before installing it.

## Replace the files and restart

Copy the replacement certificate and key to the configured learning-server paths on node1. Set the key's owner to `riak:riak` and mode to `600` as in the first lesson, then restart node1 with the two Compose files:

```sh
docker compose cp tls/server-next.crt node1:/etc/riak/learning-server.crt
docker compose cp tls/server-next.key node1:/etc/riak/learning-server.key
docker compose exec node1 chown riak:riak /etc/riak/learning-server.key
docker compose exec node1 chmod 600 /etc/riak/learning-server.key
docker compose -f compose.yaml -f compose.security.yaml restart node1
```

## Check the new connection

Repeat the authenticated curl read from the first lesson. It should succeed with the same CA trust file and credentials. Inspect the served certificate with `openssl s_client -connect 127.0.0.1:18099 -CAfile tls/ca.crt -verify_ip 127.0.0.1` and compare its serial with the replacement.

Replacing a leaf certificate does not revoke the old certificate or change the CA. A CA rotation is a separate trust transition.

## Cleanup

Stop and discard the disposable cluster when finished. If keeping it for more unauthenticated lessons, disable security through the administrative terminal, remove the exercise user and group, restore node1's saved configuration, and recreate node1 using only `compose.yaml`. Verify normal access before removing the local `tls` files.
