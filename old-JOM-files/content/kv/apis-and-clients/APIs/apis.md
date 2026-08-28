---
title: API
sidebar_label: "APIs"
date: 2026-07-22
---

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[https]: #httphttps-api
[protocol]: #protocol-buffers
[backend]: #openriak-kv-storage-backend-api

>[!MEMO]APIs
>OpenRiak has three main APIS available. HTTP/HTTPS, Protocol buffles (PB) and Backend API (storage), plus an API for Multi-Datacenter replication

## HTTP/HTTPS API

## Protocol Buffers

## OpenRiak kV storage Backend API

The OpenRiak storage API is applied accross all supported backends. The documentation in the below page is intended to be used as a guide for development of custom backend modules to ensure full compatibiltiy with OpenRiak and reduce the likelyhood of errors.

## Riak Multi-Datacenter Replication: Hooks API

This API allows applications to register replication hooks to control the following:

    * when extra objects need to be replicated along with the current object.
    * when an object should not be replicated.

## AAE Fold API

The AAE fold API allows you to execute a variety of actions/operations within Riak in accordance with your Applications requirements.