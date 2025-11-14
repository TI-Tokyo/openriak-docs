---
title: Basic Security
sidebar_label: "Basic Security"
date: 2025-11-07
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

This section covers security basics for OpenRiak with more indepth pages for various security areas available from below:

1. [Users](: ../../configure/secure/users)
2. [Networking](: ../../configure/secure/networking)
3. [Groups](: ../../configure/secure/groups)
4. [Sources](: ../../configure/secure/security-sources)

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

OpenRiak security may be checked, enabled, or disabled by an administrator through the command line. This allows an administrator to change security settings for the whole cluster quickly without needing to change settings on a node-by-node basis.

### Note: Currently, OpenRiak security commands can be run only through the command line, using the riak admin security command. In future versions of OpenRiak, administrators may have the option of issuing those commands through the Protocol Buffers and HTTP interfaces.

## Enabling security

**Warning: Enable security with caution**

>Enabling security will change the way your client libraries and your applications interact with Riak.

>Once security is enabled, all client connections must be encrypted and all permissions will be denied by default. Do not enable this in production until you have worked through the security checklist above and tested everything in a non-production environment.


OpenRiak security is disabled by default. To enable it:

```bash
riak admin security enable
```

As per the warning above, do not enable security in production without taking the appropriate precautions.

All users, groups, authentication sources, and permissions can be configured while security is disabled, which will allow you to create a security configuration with any level of complexity without prematurely impacting the service. This should be considered when you are managing users and managing sources.

## Disabling Security

### Note: While security is disabled, clients will need to be reconfigured to no longer require TLS and send credentials.

If you disable security, this means that you have disabled all of the various permissions checks that take place when executing operations against OpenRiak. Users, groups, and other security attributes remain available for configuration while security is disabled, and will be applied if and when security is re-enabled.

```bash
riak admin security disable
```

### Note: While security is disabled, clients will need to be reconfigured to no longer require TLS and send credentials.

# Managing Permissions

This section gives a general over view of how to grant/revoke permissions from a user, group etc. For more details on manage users see [here](: ../../configure/secure/users).

## Grant and Revoke

Permission to perform a wide variety of operations against OpenRiak can be granted to—or revoked from—users via the `grant` and `revoke` commands.

The grant command takes one of the following forms:

```bash
riak admin security grant <permissions> on any to all|{<user>|<group>[,...]}
riak admin security grant <permissions> on <bucket-type> to all|{<user>|<group>[,...]}
riak admin security grant <permissions> on <bucket-type> <bucket> to all|{<user>|<group>[,...]}
```

The revoke command is essentially the same, except that `to` is replaced with `from`:

```bash
riak admin security revoke <permissions> on any from all|{<user>|<group>[,...]}
riak admin security revoke <permissions> on <bucket-type> from all|{<user>|<group>[,...]}
riak admin security revoke <permissions> on <bucket-type> <bucket> from all|{<user>|<group>[,...]}
```

If you select `any`, this means that the permission (or set of permissions) is granted/revoked for all buckets and bucket-types. If you specify a bucket type only, then the permission is granted/revoked for all buckets of that type. If you specify a bucket type and a bucket, the permission is granted/revoked only for that bucket type/bucket combination.

### Note: You cannot grant/revoke permissions with respect to a bucket alone. You must specify either a bucket type by itself or a bucket type and bucket. This limitation reflects the naming structure underlying buckets and bucket types

Selecting `all` grants or revokes a permission (or set of permissions) for all users in all groups. When specifying the user(s)/group(s) to which you want to apply a permission (or set of permissions), you may list any number of users or groups comma-separated with no whitespace.

If the same name is used for both a user and a group, the `grant` command will ask for the name to be prefixed with `user/` or `group/` to disambiguate.

## Key/Value Permissions
These permissions can be granted for basic key/value access functionality:

|----------------------|---------------------------------------------------|
| Permission           | Operation                                         |
|----------------------|---------------------------------------------------|
| riak_kv.get          | Retrieve objects                                  |
| riak_kv.put          | Create or update objects                          |
| riak_kv.delete       | Delete objects                                    |
| riak_kv.index        | Index objects using secondary indexes (2i)        |
| riak_kv.list_keys    | List all of the keys in a bucket                  |
| riak_kv.list_buckets | List all buckets                                  |
|----------------------|---------------------------------------------------|

If you’d like to create, for example, a `client` account that is allowed only to run `GET` and `PUT` requests on all buckets:

```bash
riak admin security add-user client
riak admin security grant riak_kv.get,riak_kv.put on any to client
```

# MapReduce Permissions

Permission to perform MapReduce jobs can be assigned using `riak_kv.mapreduce`. The following example grants MapReduce permissions to the user `mapreduce-power-user` for all buckets and bucket types:

```bash
riak admin security grant riak_kv.mapreduce on any to mapreduce-power-user
```

# Bucket Type Permissions

|----------------------------|-----------------------------------------------------------|
| Permission                 | Operation                                                 |
|----------------------------|-----------------------------------------------------------|
| riak_core.get_bucket       | Retrieve the props associated with a bucket               |
| riak_core.set_bucket       | Modify the props associated with a bucket                 |
| riak_core.get_bucket_type  | Retrieve the set of props associated with a bucket type   |
| riak_core.set_bucket_type  | Modify the set of props associated with a bucket type     |
|----------------------------|-----------------------------------------------------------|


# Managing Sources

While user management enables you to control authorization with regard to users, security sources provide you with an interface for managing means of authentication. If you create users and grant them access to some or all of Riak’s functionality as described in the [User](: ../../configure/secure/users) section, you will then need to define security sources required for authentication.

More information on Security sources can be found [here](: ../../configure/secure/security-sources)

## Add source

OpenRiak security sources may be applied to a specific user, multiple users, or all users (all).

|-------------|-----------------------------------------------------------------------------------------------------------------|
| Source      | Description                                                                                                     |
|-------------|-----------------------------------------------------------------------------------------------------------------|
| trust       | Always authenticates successfully if access has been granted to a user or all users on the specified CIDR range |
| password    | Check the user’s password against the PBKFD2-hashed password stored in Riak                                     |
| pam         | Authenticate against the given pluggable authentication module (PAM) service                                    |
| certificate | Authenticate using a client certificate                                                                         |
|-------------|-----------------------------------------------------------------------------------------------------------------|

# Security Ciphers

# Enabling SSL

# TLS Settings

# Certificate Configuration

# Referer Checks and Certificate Revocation Lists

