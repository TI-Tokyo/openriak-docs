---
title: Basic Security
sidebar_label: "Basic Security"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

This section covers a variety of basic security items, with more indepth pages for Networking and Users available from below:

1. [Users](: ../../configure/secure/users)
2. [Networking](: ../../configure/secure/networking)

# Introduction

OpenRiak administrators can selectively apportion access to a wide variety of OpenRiak’s functionality, including accessing, modifying, and deleting objects, changing bucket properties, and running MapReduce jobs.

## Terminology
* Authentication is the process of identifying a user.
* Authorization is verifying whether a user has access to perform the requested operation.
* Groups can have permissions assigned to them, but cannot be authenticated.
* Users can be authenticated and authorized; permissions (authorization) may be granted directly or via group membership. See [here](: ../../configure/secure/users) for further information.
* Sources are used to define authentication mechanisms. A user cannot be authenticated to OpenRiak until a source is defined.

# Security Checklist

There are a few key steps that all applications will need to undertake when turning on OpenRiak security. Missing one of these steps will almost certainly break your application, so make sure that you have done each of the following before enabling security:

1. Because OpenRiak security requires a secure SSL connection, you will need to generate appropriate SSL certs, enable SSL and establish a certificate configuration on each node. If you enable security without having established a functioning SSL connection, all requests to Riak will fail.
2. Define users and, optionally, groups
3. Define an authentication source for each user
4. Grant the necessary permissions to each user (and/or group)
5. Check any Erlang MapReduce code for invocations of OpenRiak modules other than riak_kv_mapreduce. Enabling security will prevent those from succeeding unless those modules are available via the add_path mechanism documented in Installing Custom Code.
6. Make sure that your client software will work properly:
7. It must pass authentication information with each request
8. It must support HTTPS or encrypted Protocol Buffers traffic
9. If using HTTPS, the proper port (presumably 443) is open from client to server
10. Code that uses Riak’s deprecated link walking feature will not work with security enabled
11. If you have applications that rely on an already existing Riak cluster, make sure that those applications are prepared to gracefully transition into using OpenRiak security once security is enabled.

Security should be enabled only after all of the above steps have been performed and your security setup has been properly vetted.

Clients that use Protocol Buffers will typically have to be reconfigured/restarted with the proper credentials once security is enabled.

# Security Basics

# Managing Permissions

# MapReduce Permissions

# Bucket Type Permissions

# Managing Sources

# Security Ciphers

# Enabling SSL

# TLS Settings

# Certificate Configuration

# Referer Checks and Certificate Revocation Lists

