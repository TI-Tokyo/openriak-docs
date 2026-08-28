---
title: 'Authenticate an application client'
description: 'Show developers how to authenticate an application client with a minimal verified example.'
weight: 2
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\erlang.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\java.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\php.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\python.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\security\ruby.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show developers how to authenticate an application client with a minimal verified example.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Client Security

Versions of Riak 2.0 and later come equipped with a [security subsystem]({{< baseurl >}}kv/3.4.1/how-to/secure/enable-security/) that enables you to choose

* which Riak users/clients are authorized to perform a wide variety of
  Riak operations, and
* how those users/clients are required to authenticate themselves.

The following four authentication mechanisms, aka [security sources]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) are available:

* [Trust]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#trust-based-authentication)-based
  authentication enables you to specify trusted
  [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)s
  from which all clients will be authenticated by default
* [Password]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#password-based-authentication)-based authentication requires
  that clients provide a username and password
* [Certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication
  requires that clients
* [Pluggable authentication module (PAM)]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication)-based authentication requires
  clients to authenticate using the PAM service specified using the
  [`riak admin security`]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/)
  command line interface

OpenRiak's approach to security is highly flexible. If you choose to use
OpenRiak's security feature, you do not need to require that all clients
authenticate via the same means. Instead, you can specify authentication
sources on a client-by-client, i.e. user-by-user, basis. This means that
you can require clients performing, say, [MapReduce]({{< baseurl >}}kv/3.4.1/how-to/develop/run-mapreduce/)
operations to use certificate auth, while clients performing [K/V Operations]({{< baseurl >}}kv/3.4.1/how-to/develop/) have to use username and password. The approach
that you adopt will depend on your security needs.

This document provides a general overview of how that works. For
managing security in Riak itself, see the following documents:

* [Authentication and Authorization]({{< baseurl >}}kv/3.4.1/how-to/secure/enable-security/)
* [Managing Security Sources]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/)

We also provide client-library-specific guides for the following
officially supported clients:

* [Java]({{< baseurl >}}kv/3.4.1/how-to/develop/authenticate-client/)
* [Ruby]({{< baseurl >}}kv/3.4.1/how-to/develop/authenticate-client/)
* [PHP]({{< baseurl >}}kv/3.4.1/how-to/develop/authenticate-client/)
* [Python]({{< baseurl >}}kv/3.4.1/how-to/develop/authenticate-client/)
* [Erlang]({{< baseurl >}}kv/3.4.1/how-to/develop/authenticate-client/)

#### Certificates, Keys, and Authorities

If Riak security is enabled, all client operations, regardless of the
security source you choose for those clients, must be over a secure SSL
connection. If you are using a self-generated Certificate Authority
(CA), Riak and connecting clients will need to share that CA.

To use certificate-based auth, you will need to create a Public Key
Infrastructure (PKI) based on
[x.509](http://en.wikipedia.org/wiki/X.509) certificates. The central
foundation of your PKI should be a Certificate Authority (CA), created
inside of a secure environment, that can be used to sign certificates.
In addition to a CA, your client will need to have access to a private
key shared only by the client and Riak as well as a CA-generated
certificate.

To prevent so-called [Man-in-the-Middle
attacks](http://en.wikipedia.org/wiki/Man-in-the-middle_attack), private
keys should never be shared beyond Riak and connecting clients.

> **HTTP not supported**
>
> Certificate-based authentication is available only through OpenRiak's
[Protocol Buffers]({{< baseurl >}}kv/3.4.1/reference/protocol-buffers/) interface. It is not available through the
[HTTP API]({{< baseurl >}}kv/3.4.1/reference/http-api/).

##### Default Names

In OpenRiak's [configuration files]({{< baseurl >}}kv/3.4.1/reference/configuration/#security), the
default certificate file names are as follows:

Cert | Filename
:----|:-------
Certificate authority (CA) | `cacertfile.pem`
Private key | `key.pem`
CA-generated cert | `cert.pem`

These filenames will be used in the client-library-specific tutorials.

### Erlang

This tutorial shows you how to set up a Riak Erlang client to
authenticate itself when connecting to Riak.

If you are using [trust]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/), [PAM-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication), you can use the security setup described [below](#erlang-client-basics). [Password]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#password-based-authentication)-based authentication is covered
in a [later section](#password-based-authentication). If you are using
[certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication, follow
the instructions in the [section below](#certificate-based-authentication).

**Note on certificate generation**
This tutorial does not cover certificate generation. It assumes that all
necessary certificates have already been created and are stored in a directory
called `/ssl_dir`. This directory name is used only for example purposes.

#### Erlang Client Basics

When connecting to Riak using an Erlang-based client, you typically use
a process identifier to refer to the client connection. The following
example creates a process identifier (we'll call it `Pid`) for a
connection to `localhost` on port 8087:

```erlang
{ok, Pid} = riakc_pb_socket:start("127.0.0.1", 8087).
```

If you are using Riak security, _all_ connecting clients should have
access to the same Certificate Authority (CA) used on the server side,
regardless of which [security source]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) you
choose. In addition, all clients should provide a username. The example
above created a connection to Riak without specifying a username or CA.
That information is specified as a list of options passed to the
`start` function. We'll specify those options in a list called
`SecurityOptions`.

```erlang
CertDir = "/ssl_dir",
SecurityOptions = [
                   {credentials, "riakuser", ""},
                   {cacertfile, filename:join([CertDir, "cacertfile.pem"])}
                  ],
{ok, Pid} = riakc_pb_socket:start("127.0.0.1", 8087, SecurityOptions).
```

Please note that you do not need to specify a password if you are not
using password-based authentication. If you are using a different
security source, Riak will ignore the password. You can enter an empty
string (as in the example above) or anything you'd like.

This client is not currently set up to use any of the available security
sources, with the exception of trust-based authentication, provided that
the [CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
from which the client is connecting has been specified as trusted. More
on specifying trusted CIDRs can be found in [Trust-based Authentication]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#trust-based-authentication).

#### Password-based Authentication

To enable our client to use password-based auth, we can use most of the
information from the example above, with the exception that we'll also
specify a password for the client in the `SecurityOptions` list from
above. We'll use the password `rosebud` here and in the rest of the
examples.

```erlang
CertDir = "/ssl_dir",
SecurityOptions = [
                   {credentials, "riakuser", "rosebud"},
                   {cacertfile, filename:join([CertDir, "cacertfile.pem"])}
                  ],
{ok, Pid} = riakc_pb_socket:start("127.0.0.1", 8087, SecurityOptions).
```

#### PAM-based Authentication

If you have specified that a specific client be authenticated using
[PAM]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication), you will
need to provide a CA as well as the username and password that you
specified when creating the user in Riak. For more, see our
documentation on [User Management]({{< baseurl >}}kv/3.4.1/how-to/secure/enable-security/#user-management).

#### Certificate-based Authentication

Using certificate-based authentication requires us to specify the
location of a general CA (as with all security sources), a username, a
CA-generated cert, and a private key. We'll assume that all certs are
stored in `/ssl_dir`, as in the previous examples.

```erlang
CertDir = "/ssl_dir",
SecurityOptions = [
                   {credentials, "riakuser", "rosebud"},
                   {cacertfile, filename:join([CertDir, "cacertfile.pem"])},
                   {certfile, filename:join([CertDir, "cert.pem"])},
                   {keyfile, filename:join([CertDir, "key.pem"])}
                  ],
{ok, Pid} = riakc_pb_socket:start("127.0.0.1", 8087, SecurityOptions).
```

### Java

This tutorial shows you how to set up a Riak Java client to authenticate
itself when connecting to Riak.

If you are using [trust-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#trust-based-authentication) or [PAM]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication)-based authentication, you can use the
security setup described [below](#java-client-basics). [Certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication is not
yet supported in the Java client.

#### Java Client Basics

When connecting to Riak using a Java-based client, you typically do so
by instantiating separate `RiakNode` objects for each node in your
cluster, a `RiakCluster` object registering those `RiakNode` objects,
and finally a `RiakClient` object that registers the general cluster
configuration. In this document, we will be working with only one node.

If you are using Riak security, _all_ connecting clients should have
access to the same Certificate Authority (CA) used on the server side,
regardless of which [security source]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) you
choose. All clients should also provide a username, regardless of
security source. The example below sets up a single node object (we'll
simply call it `node`) that connects to Riak on `localhost` and on port
8087 and specifies `riakuser` as a username. That object will be used to
create a cluster object (we'll call it `cluster`), which will in turn be
used to create a `client` object. The setup below does not specify a CA:

```java
import com.basho.riak.client.api.RiakClient;
import com.basho.riak.client.api.RiakCluster;
import com.basho.riak.client.api.RiakNode;

RiakNode node = new RiakNode.Builder()
        .withRemoteAddress("127.0.0.1")
        .withRemotePort(8087)
        // This will specify a username but no password or keystore:
        .withAuth("riakuser", null, null)
        .build();

RiakCluster cluster = new RiakCluster.Builder(node)
        .build();

RiakClient client = new RiakClient(cluster);
```

This client object is not currently set up to use any of the available
security sources. This will change in the sections below.

To enable our client to use password-based auth, we can use most of the
setup from the example above, with the exception that we will specify a
password for the client in the `withAuth` method in the `node` object's
constructor rather than leaving it as `null`. We will also pass a
`KeyStore` object into that method.

```java
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.KeyStore;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;

// Generate an InputStream from the CA cert
InputStream inputStream = new InputStream("/ssl_dir/cacertfile.pem");

// Generate an X509Certificate from the InputStream and close the stream
CertificateFactory certFactory = CertificateFactory.getInstance("X.509");
X509Certificate caCert = (X509Certificate) certFactory.generateCertificate(inputStream);
inputStream.close();

// Generate a KeyStore object
KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
ks.load(null, "password".toCharArray());
ks.setCertificateEntry("cacert", caCert);

RiakNode node = new RiakNode.Builder()
        .withRemoteAddress("127.0.0.1")
        .withRemotePort(8087)
        .withAuth("riakuser", "rosebud", ks)
        .build();

// Construct the cluster and client object in the same fashion as above
```

#### PAM- and Trust-based Authentication

If you are using PAM- or trust-based authentication, the only difference
from password-based authentication is that you do not need to specify a
password.

Certificate-based authentication is not currently supported in the
official Riak Java client.

### PHP

This tutorial shows you how to set up a Riak PHP client to authenticate
itself when connecting to Riak.

If you are using [trust-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#trust-based-authentication) or [PAM]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication)-based authentication, you can use the
security setup described [below](#php-client-basics). [Certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication is not
yet supported in the PHP client due to limitations of the HTTP interface of Riak.

#### PHP Client Basics

When connecting to Riak using a PHP-based client, you typically do so
by instantiating separate `\Basho\Riak\Node` objects for each node in your
cluster and passing those `\Basho\Riak\Node` objects as an array to a
`\Basho\Riak` object as a dependency. In this document, we will be working with
only one node.

If you are using Riak security, _all_ connecting clients should have
access to the same Certificate Authority (CA) used on the server side,
regardless of which [security source]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) you choose. All clients should also provide a username, regardless of
security source. The example below sets up a single node object (we'll
simply call it `node`) that connects to Riak on `localhost` and on port
8087 and specifies `riakuser` as a username. That object will be used to
create a Riak object. The setup below does not specify a CA and will throw
an `\Basho\Riak\Node\Builder\Exception`:

```php
use \Basho\Riak;
use \Basho\Riak\Node;

$node = (new Node\Builder())
    ->atHost('127.0.0.1')
    ->onPort('8087')
    ->usingPasswordAuthentication('riakuser')
    ->build();

// since we are using a single node, it needs to be wrapped in array brackets
$riak = new Riak([$node]);
```

To enable our client to use password-based auth, we can use most of the
setup from the example above, with the exception that we will specify a
password for the client in the `usingPasswordAuthentication` method in
the `node` object's builder rather than omitting it. We will also
pass the path of the CA file relative to the current working directory into
the `withCertificateAuthorityFile` method.

$node = (new Node\Builder())
    ->atHost('127.0.0.1')
    ->onPort('8087')
    ->usingPasswordAuthentication('riakuser', 'rosebud')
    ->withCertificateAuthorityFile(getcwd() . '/ssl_dir/cacertfile.pem')
    ->build();

If you are using PAM- or trust-based authentication, the only difference
from password-based authentication is that you do not need to specify a
password. There are helper methods that handle this for you,
`usingPamAuthentication` and `usingTrustAuthentication`.

// PAM Example
$node = (new Node\Builder())
    ->atHost('127.0.0.1')
    ->onPort('8087')
    ->usingPamAuthentication('riakuser')
    ->withCertificateAuthorityFile(getcwd() . '/ssl_dir/cacertfile.pem')
    ->build();

// Trust Example
$node = (new Node\Builder())
    ->atHost('127.0.0.1')
    ->onPort('8087')
    ->usingTrustAuthentication('riakuser')
    ->withCertificateAuthorityFile(getcwd() . '/ssl_dir/cacertfile.pem')
    ->build();

Certificate-based authentication is not currently supported in the
official Riak PHP client due to limitations in the HTTP interface.

### Python

This tutorial shows you how to set up a Riak Python client to
authenticate itself when connecting to Riak.

If you are using [trust-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) or [PAM-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication), you can use the security
setup described [below](#python-client-basics). [Password]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#password-based-authentication)-based authentication is covered
in a [later section](#password-based-authentication). If you are using
[certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication, follow
the instructions in the [section below](#certificate-based-authentication).

#### OpenSSL Versions

The Riak Python client requires that you install OpenSSL 1.0.1g or
later. If you have an earlier version installed, you will receive a
warning along the following lines:

```
Found OpenSSL 0.9.8za 5 Jun 2014 version, but expected at least OpenSSL 1.0.1g.  Security may not support TLS 1.2.
```

#### Python Client Basics

When connecting to Riak using a Python-based client, you typically
instantiate an object from the `RiakClient` class that then handles all
interactions with Riak. All authentication-related information that
needs to be used by the client object can be passed to the object upon
instantiation by creating a `SecurityCreds` object.

If you are using Riak Security, _all_ connecting clients should have
access to the same Certificate Authority (CA) used on the server side,
regardless of which [security source]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) you
choose. All clients should also provide a username. The example below
sets up a client object (we'll simply call it `client`) that connects to
Riak on `localhost` and on port 8087 without any security credentials:

```python
from riak import RiakClient

client = RiakClient(host='127.0.0.1', pb_port=8087)
```

To provide security credentials, we'll create an object called `creds`
and specify `riakuser` as the username. We'll also point the client to a
CA stored at `/ssl_dir/cacertfile.pem`.

```python
creds = SecurityCreds(username='riakuser',
                      cacert_file='/ssl_dir/cacertfile.pem')
```

Now we can specify those credentials when we create our `client` object.

```python
client = RiakClient(host='127.0.0.1', pb_port=8087, credentials=creds)
```

This client object is not currently set up to use any of the
available security sources with the exception of trust-based auth,
provided that the
[CIDR](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) from
which the client is connecting has been specified as trusted. More on
specifying trusted CIDRs can be found in [Trust-based
Authentication]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/).

**Note**: The examples in the following sections specify certs on the
basis of their filepaths, e.g. `/ssl_dir/cacertfile.pem`. In addition to
specifying certs by location, you can also provide OpenSSL objects
instead. You can find out how to do so in [Using OpenSSL Objects](#using-openssl-objects) below.

To enable our client to use password-based auth, we can use most of the
information from the above, with the exception that we'll also specify a
password for the client in the `creds` object from above. We'll use the
password `rosebud` here and in the rest of the examples.

```python
creds = SecurityCreds(username='riakuser',
                      cacert_file='/ssl_dir/cacertfile.pem',
                      password='rosebud')
```

Using certificated-based authentication requires us to specify the
location of a general CA (as with all security sources), a username, a
CA-generated cert, and a private key. We'll assume that all certs are
stored in `/ssl_dir`, as in the previous examples.

```python
creds = SecurityCreds(username='riakuser',
                      cacert_file='/ssl_dir/cacertfile.pem',
                      cert_file='/ssl_dir/cert.pem',
                      pkey_file='/ssl_dir/key.pem')
```

#### Specifying a Certificate Revocation List

If you are using a CA-generated Certificate Revocation List (CRL), you
can specify its filepath using the `crl_file` parameter.

```python
creds = SecurityCreds(username='riakuser',
                      # Using the cert information from above
                      crl_file='/ssl_dir/revocation.crl')
```

#### Specifying Ciphers

To specify a list of preferred [security ciphers]({{< baseurl >}}kv/3.4.1/how-to/secure/enable-security/#security-ciphers), you can pass in a colon-delimited
string to the `ciphers` parameter:

```python
creds = SecurityCreds(username='riakuser',
                      # Using the cert information from above
                      ciphers='X-CIPHER-1:X-CIPHER-2:X-CIPHER-3:ETC')
```

#### Using OpenSSL Objects

Whenever you specify certs, you have the option of either passing in
file paths as strings (as in the examples above) or properly created
OpenSSL objects, e.g. objects created using the
[pyOpenSSL](https://pyopenssl.readthedocs.org/en/latest/) library. If
you generate OpenSSL objects this way, you should note that they must
be specified differently when creating a `SecurityCreds` object. The
table below lists the appropriate parameter names for each method, as
well as the pyOpenSSL class to which each cert must belong if you create
OpenSSL objects.

Cert | File path | OpenSSL object | Class
:----|:----------|:---------------|:-----
Certificate Authority (CA) | `cacert_file` | `cacert` | `OpenSSL.crypto.X509`
Private key | `key_file` | `key` | `OpenSSL.crypto.PKey`
CA-generated cert | `cert` | `cert_file` | `OpenSSL.crypto.X509`
CRL | `crl` | `crl_file` | `OpenSSL.crypto.CRL`

If you specify filepaths, the appropriate certs will be loaded and
converted into the appropriate OpenSSL object. The functions used for
this are `OpenSSL.crypto.load_privatekey()` for the private key and
`OpenSSL.crypto.load_certificate` for the cert and CA cert.

### Ruby

This tutorial shows you how to set up a Riak Ruby client to authenticate
itself when connecting to Riak.

If you are using [trust-]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) or [PAM]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#pam-based-authentication)-based authentication, you
can use the security setup described in the [Ruby Client Basics](#ruby-client-basics) section.
[Password]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#password-based-authentication)-based authentication is covered
in a [later section](#password-based-authentication), while [certificate]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#certificate-based-authentication)-based authentication
is covered [further down](#certificate-based-authentication).

#### Ruby Client Basics

When connecting to Riak using a Ruby-based client, you must instantiate
an object from the `Riak::Client` class that then handles interactions
with Riak (you may have more than one client object active in an
application if you wish). All authentication-related information that
needs to be used can be passed to the object upon instantiation in an
`authentication` hash.

If you are using Riak Security, _all_ connecting clients should have
access to the same Certificate Authority (CA) used on the server side,
regardless of which [security source]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/) you choose. All clients should also provide a username. The example below sets up a client object (we'll simply call it `client`) that connects
to Riak on `localhost` and on port 8087, specifies `riakuser` as a
username, and points the client to a CA located at
`/ssl_dir/cacertfile.pem`.

```ruby
require 'riak'

client = Riak::Client.new(
  host: '127.0.0.1',
  pb_port: 8087,
  authentication: {
    ca_file: '/ssl_dir/cacertfile.pem',
    user: 'riakuser'
  }
)
```

This client object is currently not set up to use any of the available
security sources, except trust-based auth, provided that the CIDR from
which the client is connecting has been specified as trusted. More on
this in [Trust-based Authentication]({{< baseurl >}}kv/3.4.1/how-to/secure/manage-sources/#trust-based-authentication).

To enable our client to use password-based auth, we can use most of the
information from the example above, with the exception that we will
specify a password for the client in the `authentication` hash. We'll
use the password `rosebud` here and in the rest of the examples.

```ruby
client = Riak::Client.new(
  # Using the host and pb_port from above
  authentication: {
    ca_file: '/ssl_dir/cacertfile.pem',
    user: 'riakuser',
    password: 'rosebud'
  }
)
```

Using certificate-based authentication requires us to specify the
location of a CA (as with all security sources), a username, a
client-specific CA, a CA-generated cert, and a private key. We'll assume
that all certs are stored in `/ssl_dir`, as in the previous examples.

```ruby
client = Riak::Client.new(
  # Using the host and pb_port from above
  authentication: {
    ca_file: '/path/to/cacertfile.pem',
    user: 'riakuser',
    client_ca: '/path/to/client_cert.pem',
    cert: '/path/to/cert.pem',
    key: '/path/to/key.pem'
  }
)
```

The `client_ca` must be specified if you intend to use a CA that is
different from the CA used by Riak, e.g. if you are integrating with
an existing single sign-on (SSO) system. If the client and server CA are
the same, you don't need to specify `client_ca`. The client cert and
key, however, must always be specified.

The `client_ca`, `cert`, and `key` fields are all flexible in their
usage. You can use a string specifying a filename (as in the example
above), or you can pass in an appropriate OpenSSL object, e.g. an SSL
object created using the
[OpenSSL](http://ruby-doc.org/stdlib-2.0/libdoc/openssl/rdoc/OpenSSL.html)
gem. If you use specify filenames, those files will be loaded and
converted into the appropriate OpenSSL object.

If you create certificates specifying a CA-signed Certificate Revocation
List (CRL), those certs will be checked against the CRLs specified. You
can specify the location of the list in the `authentication` hash:

```ruby
client = Riak::Client.new(
  # Using the host and pb_port from above
  authentication: {
    ca_file: '/ssl_dir/cacertfile.pem',
    user: 'riakuser',
    # Using the cert paths from above
    crl_file: '/ssl_dir/revocation.crl'
  }
)
```

CRL checking can sometimes be a slow process. To disable it, you can set
`crl` to `false` in the `authentication` hash when instantiating your
client object.

#### Online Certificate Status Protocol

If you create certificates with a specified Online Certificate Status
Protocol
([OCSP](http://en.wikipedia.org/wiki/Online_Certificate_Status_Protocol)),
the OCSP endpoint will automatically be checked. If that endpoint is not
available or if checking is running slowly, you can disable OCSP
checking by setting `ocsp` to `false` in the `authentication` hash.

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
