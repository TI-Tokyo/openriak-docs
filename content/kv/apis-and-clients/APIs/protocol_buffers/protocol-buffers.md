---
title: Protocol Buffers
sidebar_label: "Protocol Buffers"
date: 2026-07-29
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[protocol]: #protocol
[whatmakesop]: #what-makes-up-an-operation


>[!MEMO]This is an overview of the operations that can be performed using the Protocol Buffers Client (PBC) for OpenRiak.
>It can also be used as a guide for developed a PBC-compatible OpenRiak client.

# Protocol

By default, OpenRiak listens on TCP port 8087 (This can be changed in your `riak.conf` file) for incomming connections. Once a connection has been established, the client can send a stream of requests on the same connection.

## What makes up an operation?

Each operation consists of a (request message)[https://protobuf.dev/programming-guides/encoding/] and one or more response messages. Messages are all encoded the same way, consisting of:

    * 32-bit length of message code + Protocol Buffers message in network order
    * 8-bit message code to identify the Protocol Buffers message
    * N bytes of Protocol Buffers-encoded message

    