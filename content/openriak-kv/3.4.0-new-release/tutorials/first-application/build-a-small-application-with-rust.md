---
title: Build a small application with Rust
description: Build a small HTTP client that creates a profile, reads and updates it with causal context, finds it
  by an index, and deletes it.
weight: 130
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
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
- tutorials/first-application/rust.md
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- tutorials/data-and-concurrency/create-and-resolve-concurrent-updates
- reference/client-libraries/rust-client
- reference/http-api/fetch-object
- reference/http-api/store-object
- reference/http-api/secondary-index-queries
- foundations/data-and-consistency/objects-keys-and-buckets
- foundations/data-and-consistency/causality-version-vectors-and-siblings
---

Build a small HTTP client that creates a profile, reads and updates it with causal context, finds it by an index, and deletes it.

## Prepare

Use the Leveled cluster from the Docker tutorial and **Rust with Cargo; reqwest 0.12.24**. This exercise uses a local unauthenticated HTTP listener. Use the authentication guide before connecting this client to a secured deployment.

Run `cargo new openriak-learning-client`, enter that directory, and replace `src/main.rs` with the example. Add these dependencies to `Cargo.toml`, then retain `Cargo.lock` for repeatable builds:

```toml
[dependencies]
reqwest = { version = "=0.12.24", default-features = false, features = ["blocking", "json", "rustls-tls"] }
serde_json = "1.0"
```

The example uses the untyped `client-demo` bucket and the key `aiko`. Run one language example at a time so they do not overwrite one another's exercise data. The index and request timeout are deliberate example choices.

## Run the application

{{< learning-example file="main.rs" language="rust" >}}

```sh
export RIAK_HTTP=http://127.0.0.1:18098
cargo run
```

## Check the result

The program prints the original profile, an index response containing `aiko`, and `Updated, indexed, and deleted aiko`. It fetches the object again after the update and checks the changed name before deletion.

The update carries the context from the preceding read and resubmits the intended index metadata. If an HTTP error occurs, inspect the status and body before retrying; an empty successful PUT response is normal.

## Cleanup and next steps

A successful run deletes its object. After an interrupted run, inspect `/buckets/client-demo/keys/aiko` and delete that exercise object if it remains. Continue with the concurrency tutorial to handle sibling responses and competing writers.

The underlying [HTTP library API](https://docs.rs/reqwest/0.12.24/reqwest/blocking/index.html) documents connection, TLS, and timeout options.
