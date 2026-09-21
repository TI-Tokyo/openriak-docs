---
title: Make an authenticated TLS client connection
description: Create a local certificate authority, enable an HTTPS listener, and authenticate a read-only user.
  Use the disposable Docker learning cluster; these changes enable security for that cluster.
weight: 370
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
- new-developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/security/secure-client-connection.md
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- tutorials/security/apply-and-test-group-permissions
- how-to/security/enable-authentication-and-authorization
- how-to/security/configure-and-rotate-tls-certificates
- reference/configuration/authentication-authorization-and-tls-settings
- foundations/security/security-boundaries-and-trust
- foundations/security/identities-authentication-and-permissions
- foundations/security/tls-and-certificate-trust
next_page: tutorials/security/apply-and-test-group-permissions
---

Create a local certificate authority, enable an HTTPS listener, and authenticate a read-only user. Use the disposable Docker learning cluster; these changes enable security for that cluster.

## Prepare

Complete the earlier cluster and object exercises. Open a Bash terminal in the Compose directory and run `source learning-env.sh`. You need OpenSSL on the host. Keep the local administrative terminal open throughout the exercise.

Save a copy of node1's `riak.conf` before editing it. Write a known test object before enabling security:

```sh
curl --fail -X PUT "$RIAK_HTTP/buckets/client-demo/keys/secure"   -H 'Content-Type: text/plain' --data-binary 'TLS works'
mkdir -p tls
openssl req -x509 -newkey rsa:3072 -nodes -days 2   -keyout tls/ca.key -out tls/ca.crt -subj '/CN=OpenRiak learning CA'
openssl req -new -newkey rsa:3072 -nodes   -keyout tls/server.key -out tls/server.csr -subj '/CN=localhost'
printf 'subjectAltName=DNS:localhost,IP:127.0.0.1
' > tls/server.ext
openssl x509 -req -in tls/server.csr -CA tls/ca.crt -CAkey tls/ca.key   -CAcreateserial -days 2 -extfile tls/server.ext -out tls/server.crt
chmod 600 tls/ca.key tls/server.key
```

The short certificate lifetime and names are deliberate lab choices. Keep the CA key on the host; the node needs only the CA certificate and its own key and certificate.

## Configure node1

```sh
docker compose cp tls/ca.crt node1:/etc/riak/learning-ca.crt
docker compose cp tls/server.crt node1:/etc/riak/learning-server.crt
docker compose cp tls/server.key node1:/etc/riak/learning-server.key
docker compose exec node1 chown riak:riak /etc/riak/learning-server.key
docker compose exec node1 chmod 600 /etc/riak/learning-server.key
```

Set these explicit example values in node1's bind-mounted `config/riak.conf`, replacing any active entries for the same settings:

```riakconf
listener.https.learning = 0.0.0.0:8099
ssl.cacertfile = /etc/riak/learning-ca.crt
ssl.certfile = /etc/riak/learning-server.crt
ssl.keyfile = /etc/riak/learning-server.key
```

Create `compose.security.yaml`:

```yaml
services:
  node1:
    ports:
      - '127.0.0.1:18099:8099'
```

Run `docker compose -f compose.yaml -f compose.security.yaml up -d --no-build node1`. Wait for node1 to return and check its logs for certificate or listener errors.

## Create the reader

These credentials are only for this disposable exercise:

{{< cli-example key="shell:riak admin security add-group" prefix="kv node1" args="docs-readers" >}}

{{< cli-example key="shell:riak admin security add-user" prefix="kv node1" args="docs-reader password=docs-learning-password groups=docs-readers" >}}

{{< cli-example key="shell:riak admin security add-source" prefix="kv node1" args="docs-reader 0.0.0.0/0 password" >}}

The broad source rule is limited here by the loopback-only published port. For a shared deployment, use the actual approved client networks instead.

{{< cli-example key="shell:riak admin security grant" prefix="kv node1" args="riak_kv.get on default client-demo to docs-readers" >}}

{{< cli-example key="shell:riak admin security enable" prefix="kv node1" >}}

## Verify

```sh
curl --fail --cacert tls/ca.crt --user docs-reader:docs-learning-password   https://127.0.0.1:18099/buckets/client-demo/keys/secure
```

Expect `TLS works`. Repeat with an incorrect password and confirm rejection. Repeat without `--cacert` and confirm that the local CA is not automatically trusted; do not use `--insecure` to bypass this check.

Keep this environment for the next two security lessons. Normal unauthenticated object examples will no longer work while security is enabled.
