---
title: 'Manage authentication sources'
description: 'Show security engineers how to manage authentication sources and test the resulting controls.'
weight: 6
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'security-engineers'
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\secure\security-sources.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\managing-sources.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#enabling-security-and-restricting-source'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show security engineers how to manage authentication sources and test the resulting controls.

## Before you begin

Secure administrative access, an inventory of identities and certificates involved, and a tested rollback path that will not lock operators out.

## Overview

### Managing Security Sources

If you're looking for more general information on Riak Security, it may
be best to start with our general guide to [authentication and authorization]({{< baseurl >}}kv/3.4.0/how-to/secure/enable-security/).

This document provides more granular information on the four available
authentication sources in Riak Security: trusted networks, password,
pluggable authentication modules (PAM), and certificates. These sources
correspond to `trust`, `password`, `pam`, and `certificate`,
respectively, in the `riak admin security` interface.

The examples below will assume that the network in question is
`127.0.0.1/32` and that a Riak user named `riakuser` has been
[created]({{< baseurl >}}kv/3.4.0/how-to/secure/enable-security/#user-management) and that
security has been [enabled]({{< baseurl >}}kv/3.4.0/how-to/secure/enable-security/).

**Note on SSL connections**
If you use _any_ of the aforementioned security sources, even `trust`, you
will need to do so via a secure SSL connection.

#### Trust-based Authentication

This form of authentication enables you to specify trusted
[CIDRs](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
from which all clients will be authenticated by default.

```bash
riak admin security add-source all 127.0.0.1/32 trust
```

Produces:

```
Successfully added source
ok
```

Here, we have specified that anyone connecting to Riak from the
designated CIDR (in this case `localhost`) will be successfully
authenticated:

```curl
curl https://localhost:8098/types/<type>/buckets/<bucket>/keys/<key>
```

If this request returns `not found` or a Riak object, then things have
been set up appropriately. You can specify any number of trusted
networks in the same fashion.

You can also specify users as trusted users, as in the following
example:

```bash
riak admin security add-source riakuser 127.0.0.1/32 trust
```

Produces:

```
Successfully added source
ok
```
Now, `riakuser` can interact with Riak without providing credentials.
Here's an example in which only the username is passed to Riak:

```curl
curl -u riakuser: \
  https://localhost:8098/types/<type>/buckets/<bucket>/keys/<key>
```

##### Password-based Authentication

Authenticating via the `password` source requires that our `riakuser` be
given a password. `riakuser` can be assigned a password upon creation,
as in this example:

```bash
riak admin security add-user riakuser password=captheorem4life
```

Or a password can be assigned to an already existing user by modifying
that user's characteristics:

```bash
riak admin security alter-user riakuser password=captheorem4life
```

Produces:

```
ok

+----------+---------------+----------------------------------------+------------------------------+
| username |   member of   |                password                |           options            |
+----------+---------------+----------------------------------------+------------------------------+
| riakuser |               |652517e4703dab90f693db95acaedeec55acb530|              []              |
+----------+---------------+----------------------------------------+------------------------------+

ok
```

You can specify that _all_ users must authenticate themselves via
password when connecting to Riak from `localhost`:

```bash
riak admin security add-source all 127.0.0.1/32 password
```

Or you can specify that any number of specific users must do so:

```bash
riak admin security add-source riakuser 127.0.0.1/32 password
riak admin security add-source otheruser 127.0.0.1/32 password

#### etc
```

Now, our `riakuser` must enter a username and password to have any
access to Riak whatsoever:

```curl
curl -u riakuser:captheorem4life \
  https://localhost:8098/types/<type>/buckets/<bucket>/keys/<key>
```

##### Certificate-based Authentication

This form of authentication (`certificate`) requires that Riak and a
specified client---or clients---interacting with Riak bear certificates
signed by the same [Root Certificate
Authority](http://en.wikipedia.org/wiki/Root_certificate).

> **Note**
>
> At this time, client certificates are not supported in OpenRiak's HTTP
interface, and can be used only through the [protocol buffers interface]({{< baseurl >}}kv/3.4.0/reference/protocol-buffers/).

Let's specify that our user `riakuser` is going to be authenticated
using a certificate on `localhost`:

```bash
riak admin security add-source riakuser 127.0.0.1/32 certificate
```

When the `certificate` source is used, `riakuser` must also be entered
as the common name, aka `CN`, that you specified when you generated your
certificate, as in the following OpenSSL example:

```bash
openssl req -new ... '/CN=riakuser'
```

You can add a `certificate` source to any number of clients, as long as
their `CN` and Riak username match.

On the server side, you need to configure Riak by specifying a path to
your certificates. First, copy all relevant files to your OpenRiak cluster.
The default directory for certificates is `/etc`, though you can specify
a different directory in your [`riak.conf`]({{< baseurl >}}kv/3.4.0/reference/configuration/) by either uncommenting those lines if you choose to use the defaults or setting the paths yourself:

```riakconf
ssl.certfile = /path/to/cert.pem
ssl.keyfile = /path/to/key.pem
ssl.cacertfile = /path/to/cacert.pem
```

In the client-side example above, the client's `CN` and Riak username
needed to match. On the server (i.e. Riak) side, the `CN` specified _on
each node_ must match the node's name as registered by Riak. You can
find the node's name in [`riak.conf`]({{< baseurl >}}kv/3.4.0/reference/configuration/) under the parameter `nodename`. And so if the `nodename` for a cluster is
`riak-node-1`, you would need to generate your certificate with that in
mind, as in this OpenSSL example:

```bash
openssl req -new ... '/CN=riak-node-1'
```

Once certificates have been properly generated and configured on all of
the nodes in your OpenRiak cluster, you need to perform a [rolling restart]({{< baseurl >}}kv/3.4.0/how-to/operate/rolling-restart/). Once that process is complete, you can use the client
certificate that you generated for the user `riakuser`.

How to use Riak clients in conjunction with OpenSSL and other
certificates varies from client library to client library. We strongly
recommend checking the documentation of your client library for further
information.

##### PAM-based Authentication

This section assumes that you have set up a PAM service bearing the name
`riak_pam`, e.g. by creating a `pam.d/riak_pam` service definition
specifying `auth` and/or other PAM services set up to authenticate a
user named `riakuser`. As in the certificate-based authentication
example above, the user's name must be the same in both your
authentication module and in Riak Security.

If we want the user `riakuser` to use this PAM service on `localhost`,
we need to add a `pam` security source in Riak and specify the name of
the service:

```bash
riak admin security add-source all 127.0.0.1/32 pam service=riak_pam
```

**Note**: If you do not specify a name for your PAM service, Riak will
use the default, which is `riak`.

To verify that the source has been properly specified:

```bash
riak admin security print-sources
```

That command should output the following:

```
+--------------------+------------+----------+------------------------+
|       users        |    cidr    |  source  |        options         |
+--------------------+------------+----------+------------------------+
|      riakuser      |127.0.0.1/32|   pam    |[{"service","riak_pam"}]|
+--------------------+------------+----------+------------------------+
```

You can test that setup most easily by using `curl`. A normal request to
Riak without specifying a user will return an `Unauthorized` message:

Response:

```
<html><head><title>401 Unauthorized</title></head><body><h1>Unauthorized</h1>Unauthorized<p><hr><address>mochiweb+webmachine web server</address></body></html>
```

If you identify yourself as `riakuser` and are successfully
authenticated by your PAM service, you should get either `not found` or
a Riak object if one is stored in the specified bucket type/bucket/key
path:

```curl
curl -u riakuser:<pam_password> \
  https://localhost:8098/types/<type>/buckets/<bucket>/keys/<key>
```

##### How Sources Are Applied

When managing security sources---any of the sources explained
above---you always have the option of applying a source to either a
single user, multiple users, or all users (`all`). If specific users and
`all` have no sources in common, this presents no difficulty. But what
happens if one source is applied to `all` and a different source is
applied to a specific user?

The short answer is that the more specifically assigned source---i.e. to
the user---will be consider a user's security source. We'll illustrate
that with the following example, in which the `certificate` source is
assigned to `all`, but the `password` source is assigned to `riakuser`:

```bash
riak admin security add-source all 127.0.0.1/32 certificate
riak admin security add-source riakuser 127.0.0.1/32 password
```

If we run `riak admin security print-sources`, we'll get the following
output:

```
+--------------------+------------+-----------+----------+
|       users        |    cidr    |  source   | options  |
+--------------------+------------+-----------+----------+
|      riakuser      |127.0.0.1/32| password  |    []    |
|                    |127.0.0.1/32|certificate|    []    |
|        all         |127.0.0.1/32|certificate|    []    |
+--------------------+------------+-----------+----------+
```

As we can see, `password` is set as the security source for `riakuser`,
whereas everyone else will authenticate using `certificate`.

#### Enabling Security and Restricting Source

To provide further security, the Riak security mechanism should be enabled. This is not possible through configuration; it must be enabled via the command line:

```console
riak admin security enable
```

This is a cluster-wide setting, and will change the behaviour across the cluster with almost immediate effect.  Once security is enabled, any request to Riak sent without TLS enablement and a valid username will be blocked.

> Security enablement is not per API, both the HTTP and PB transports are impacted by enabling security, cluster-wide.

If enablement causes unexpected problems, it may be disabled again:

```console
riak admin security disable
```

Prior to Riak 3.4, some HTTP API requests could still be sent to the plain text listener after the enablement of security, and also sent without passing a valid username to the HTTPS listener.  The rest endpoints that remained insecure were: stats, AAE folds and the queue API.  This allowed operational queries to continue unimpaired by the enablement of security.

To preserve the old behaviour, and allow insecure use via HTTP of operational calls when security is enabled, the configuration option in `riak.conf` of `permit_insecure_http_ops = enabled` can be used.

> Although the CLI uses the terms `user` and `password`; these would normally translate to an `application_instance` and `shared_secret` in an actual implementation.  There is no expectation that Riak security should manage the real-world usernames and passwords of operators, developers or application end-users.

Once security is enabled, all requests will need to have a valid `user` and a valid `source`.  There are three types of `source`:

- `trust`;
  - Applies no conditions beyond a source IP address filter;
- `password`;
  - Requires the user provide a valid password, as well as matching on a source IP address filter,
  - Passwords should be assigned via the `riak admin security` CLI, as use of PAM-based authentication is deprecated.
- `certificate`;
  - Supported for **the PB API only**,
  - Requires that the username match the certificate name,
  - By inference requires the session to have included a valid client certificate in the TLS negotiation,
  - The client certificate must be signed by the same CA as the server certificate, the `ssl.cacertfile`.

A very basic setup would be:

```console
riak admin security enable
riak admin security add-user proxy_waf
riak-admin security add-source all 192.168.6.7/32 trust
```

This would permit access to the APIs only from the IP address `192.168.6.7` (this may be the address of a web application firewall, for example), and trust all access from that source as long as the username of `proxy_waf` is provided within the Authorization header.

> In this simple case, this is functionally equivalent to applying an IP filter on the node through a standard filter utility, but it is not the security equal of that measure.  An IP filter would prevent connections being made from an unauthorised host, whereas the Riak security control allows connections and requests to be sent, but blocks requests during the processing of those requests; which presents a broader attack surface.

On the PB API, a stronger level of security could be applied with:

```console
riak admin security enable
riak admin security add-user app.acme.org
riak-admin security add-source all 192.168.8.0/24 certificate
```

This would permit access from the whole of the network `192.168.8.0/24` (this may be a network hosting application instances allowed to send Riak requests) for any application instance with a valid certificate as long as the certificate name matches `app.acme.org`.

> In this case, this is functionally equivalent to requiring TLS mutual authentication on the PB API, but it is not the security equal of that measure.  A connection would still be accepted from any IP address, and an unauthenticated TLS negotiation allowed; at this stage the PB API will only accept an authentication request, and this will now only work if the IP address is valid and the certificate matches.

Further information on the configuration of security sources can be found in the [legacy documentation](https://docs.riak.com/riak/kv/latest/using/security/managing-sources/index.html).

> The use of PAM-based authentication is deprecated and may be removed in a future release.

When enabling the use of certificates, the CRL within the configured CA certificate will be checked for every connection attempt.  If there are issues with either the performance of the CRL check, or the reachability of the CRL endpoint; the crl check can be disabled via a hidden `riak.conf` setting - `check_crl = disabled`.

[Overview]: #overview
[Trust]: #trust-based-authentication
[Managing group]: {{< baseurl >}}kv/3.4.0/how-to/secure/manage-sources/

## Verify the result

Test permitted and denied access separately, validate certificate and identity details, and review security-related logs.
