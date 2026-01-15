---
title: Basic Security
sidebar_label: "Basic Security"
date: 2025-11-07
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[overview]: #overview
[terminology]: #terminology
[security checklist]: #security-checklist
[basics]: #security-basics

# Basic Security

    This section covers security basics for OpenRiak with more indepth pages for various security areas available from below:

    1. [Users](: ../../configure/secure/users)
    2. [Networking](: ../../configure/secure/networking)
    3. [Groups](: ../../configure/secure/groups)
    4. [Sources](: ../../configure/secure/security-sources)

## Overview

    OpenRiak administrators can selectively apportion access to a wide variety of OpenRiak’s functionality, including accessing, modifying, and deleting objects, changing bucket properties, and running MapReduce jobs.

## Terminology
    * Authentication is the process of identifying a user.
    * Authorization is verifying whether a user has access to perform the requested operation.
    * Groups can have permissions assigned to them, but cannot be authenticated.
    * Users can be authenticated and authorized; permissions (authorization) may be granted directly or via group membership. See [here](: ../../configure/secure/users) for further information.
    * Sources are used to define authentication mechanisms. A user cannot be authenticated to OpenRiak until a source is defined.

## Security Checklist

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

## Security Basics

OpenRiak security may be checked, enabled, or disabled by an administrator through the command line. This allows an administrator to change security settings for the whole cluster quickly without needing to change settings on a node-by-node basis.

>![NOTE] Note on OpenRiak Security commands
> Currently, OpenRiak security commands can be run only through the command line, using the riak admin security command. In future versions of OpenRiak, administrators may have the option of issuing those commands through the Protocol Buffers and HTTP interfaces.

### Enabling security

>[!caution] Enable security with caution
>Enabling security will change the way your client libraries and your applications interact with Riak.
>Once security is enabled, all client connections must be encrypted and all permissions will be denied by default. Do not enable this in production until you have worked through the security checklist above and tested everything in a non-production environment.


OpenRiak security is disabled by default. To enable it:

    ```bash
        riak admin security enable
    ```

As per the warning above, do not enable security in production without taking the appropriate precautions.

All users, groups, authentication sources, and permissions can be configured while security is disabled, which will allow you to create a security configuration with any level of complexity without prematurely impacting the service. This should be considered when you are managing users and managing sources.

### Disabling Security

>![NOTE] 
> While security is disabled, clients will need to be reconfigured to no longer require TLS and send credentials.

If you disable security, this means that you have disabled all of the various permissions checks that take place when executing operations against OpenRiak. Users, groups, and other security attributes remain available for configuration while security is disabled, and will be applied if and when security is re-enabled.

    ```bash
        riak admin security disable
    ```

### Note: While security is disabled, clients will need to be reconfigured to no longer require TLS and send credentials.

## Managing Permissions

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

>![NOTE] Note on granting/revoking permissions
>You cannot grant/revoke permissions with respect to a bucket alone. You must specify either a bucket type by itself or a bucket type and bucket. This limitation reflects the naming structure underlying buckets and bucket types

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

## MapReduce Permissions

Permission to perform MapReduce jobs can be assigned using `riak_kv.mapreduce`. The following example grants MapReduce permissions to the user `mapreduce-power-user` for all buckets and bucket types:

    ```bash
        riak admin security grant riak_kv.mapreduce on any to mapreduce-power-user
    ```

## Bucket Type Permissions

    |----------------------------|-----------------------------------------------------------|
    | Permission                 | Operation                                                 |
    |----------------------------|-----------------------------------------------------------|
    | riak_core.get_bucket       | Retrieve the props associated with a bucket               |
    | riak_core.set_bucket       | Modify the props associated with a bucket                 |
    | riak_core.get_bucket_type  | Retrieve the set of props associated with a bucket type   |
    | riak_core.set_bucket_type  | Modify the set of props associated with a bucket type     |
    |----------------------------|-----------------------------------------------------------|


## Managing Sources

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

### Example: Adding a Trusted Source

Security sources can be added either to a specific user, multiple users, or all users (all).

In general, the add-source command takes the following form:

    ```bash
        riak admin security add-source all|<users> <CIDR> <source> [<option>=<value>[...]]
    ```

Using all indicates that the authentication source can be added to all users. A source can be added to a specific user, e.g. add-source superuser, or to a list of users separated by commas, e.g. add-source jane,bill,admin.

Let’s say that we want to give all users trusted access to securables (without a password) when requests come from localhost:

    ```bash
        riak admin security add-source all 127.0.0.1/32 trust
    ```

When you check the sources with `riak admin security print-sources` command, it should output the following:

    +--------------------+------------+----------+----------+
    |       users        |    cidr    |  source  | options  |
    +--------------------+------------+----------+----------+
    |        all         |127.0.0.1/32|  trust   |    []    |
    +--------------------+------------+----------+----------+

## Security Ciphers

To view a list of currently available security ciphers or change OpenRiak’s preferences, use the `ciphers` command:

    ```bash
        riak admin security ciphers
    ```

This command will reutrn a list of available ciphers such as below:

    ```bash
        Configured ciphers

        ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256: ...

        Valid ciphers(35)

        ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256: ...

        Unknown/Unsupported ciphers(32)

        ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256: ...
    ```

 You can edit the list to restrict it or set preferred ciphers higher in the list with:

    ```bash
        riak admin security ciphers DHE-RSA-AES256-SHA:AES128-GCM-SHA256
    ```
You can then fetch an update list of ciphers:

    ```bash
        <inset list output>
    ```
A list of available ciphers for the system can be obtained with:

    ```bash
        openssl ciphers
    ```

Which will produce a similar output to:

    ```bash
    TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256: # and so on through the list.
    ```

## Client vs. Server Cipher Order

By default, OpenRiak prefers the cipher order that you set on the server, i.e. the honor_cipher_order setting is set to on. If you prefer, however, that clients’ preferred cipher order dictate which cipher is chosen, set honor_cipher_order to off.

## Enabling SSL

In order to use any authentication or authorization features, you must enable SSL for OpenRiak. SSL is disabled by default, but you will need to enable it prior to enabling security. If you are using Protocol Buffers as a transport protocol for OpenRiak, enabling SSL on a given node requires only that you specify a host and port for the node as well as a certification configuration.

If, however, you are using the HTTP API for OpenRiak and would like to configure HTTPS, you will need to not only establish a certificate configuration but also specify an HTTPS host and port. The following configuration would establish port 8088 on localhost as the HTTPS port:

    ```bash
        listener.https.$name = 127.0.0.1:8088

        # By default, "internal" is used as the "name" setting
    ```

## TLS Settings

When using Riak security, you can choose which versions of SSL/TLS are allowed. By default, only TLS 1.2 is allowed, but this version can be disabled and others enabled by setting the following configurable parameters to on or off:

* tls_protocols.tlsv1
* tls_protocols.tlsv1.1
* tls_protocols.tlsv1.2
* tls_protocols.sslv3

Three things to note:

* Among the four available options, only TLS version 1.2 is enabled by default
* You can enable more than one protocol at a time
* We strongly recommend that you do not use SSL version 3 unless absolutely necessary

## Certificate Configuration

If you are using any of the available security sources, including trust-based authentication, you will need to do so over a secure SSL connection. In order to establish a secure connection, you will need to ensure that each OpenRiak node’s configuration files point to the proper paths for your generated certs. By default, OpenRiak assumes that all certs are stored in each node’s /etc directory. you can change the location of the `/etc` directory by modifying the `platform_etc_dir`.

    |-------------------|------------------|-------------------------------------------|
    | Type              | Parameter        | Default                                   |
    |-------------------|------------------|-------------------------------------------|
    | Signing authority | ssl.cacertfile   | #(platform_etc_dir)/cacertfile.pem        |
    | Cert              | ssl.certfile     | #(platform_etc_dir)/cert.pem              |
    | Key file          | ssl.keyfile      | #(platform_etc_dir)/key.pem               |
    |-------------------|------------------|-------------------------------------------|

## Referer Checks and Certificate Revocation Lists

To protect against cross-site scripting (XSS) and request‑forgery attacks, OpenRiak enables secure referer checks by default. Those checks make it impossible to serve data directly from OpenRiak. You can turn it off by setting the  parameter to .
If certificate-based authentication is enabled, OpenRiak will check the certificate revocation list (CRL) for incoming client certificates by default. To stop Riak from performing this check, set the `check_crl` parameter to `off`.