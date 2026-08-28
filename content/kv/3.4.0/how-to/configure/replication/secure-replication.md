---
title: 'Secure replication connections'
description: 'Show operators how to secure replication connections and validate data movement.'
weight: 12
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter\ssl.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter\ssl.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\security\v2-v3-ssl-ca.md'
  - 'Legacy multi-datacenter replication terminology and commands require compatibility review.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#security-configuration'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to secure replication connections and validate data movement.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

### SSL

**Deprecation Warning**
v2 Multi-Datacenter Replication is deprecated and will be removed in a future version. Please use [v3](/kv/3.4.0/how-to/configure/replication/secure-replication/) instead.

#### Features

Riak REPL SSL support consists of the following items:

* Encryption of replication data
  * SSL certificate chain validation
  * SSL common name whitelisting support

#### SSL Configuration

To configure SSL, you will need to include the following four settings
in the `riak repl` section of your `advanced.config`:

```advancedconfig
{riak repl, [
             % ...
             {ssl_enabled, true},
             {certfile, "/full/path/to/site1-cert.pem"},
             {keyfile, "/full/path/to/site1-key.pem"},
             {cacertdir, "/full/path/to/cacertsdir"}
             % ...
            ]}

```

The `cacertdir` is a directory containing all of the CA certificates
needed to verify the CA chain back to the root.

#### Verifying Peer Certificates

Verification of a peer's certificate common name *(CN)* is enabled by using
the `peer_common_name_acl` property in the `riak_repl` section of your
`advanced.config` to specify an Access Control List *(ACL)*.

The ACL is a list of one or more *patterns*, separated by commas. Each
pattern may be either the exact CN of a certificate to allow, or a
wildcard in the form `*.some.domain.name`. Pattern comparison is
case-insensitive, and a CN matching any of the patterns is allowed to connect.

For example, `["*.corp.com"]` would match `site3.corp.com` but not
`foo.bar.corp.com` or `corp.com`. If the ACL were
`["*.corp.com", "foo.bar.corp.com"]`, `site3.corp.com` and `foo.bar.corp.com`
would be allowed to connect, but `corp.com` still would not.

If no ACL (or only the special value `"*"`) is specified, no CN filtering
is performed, except as described below.

**Identical Local and Peer Common Names**
As a special case supporting the view that a host's CN is a fully-qualified
domain name that uniquely identifies a single network device, if the CNs of
the local and peer certificates are the same, the nodes will *NOT* be allowed
to connect.

This evaluation supercedes ACL checks, so it cannot be overridden with any
setting of the `peer_common_name_acl` property.

##### Examples

The following example will only allow connections from peer certificate
names like `db.bashosamplecorp.com` and `security.bashosamplecorp.com`:

```advancedconfig
{riak_repl, [
             % ...
             {peer_common_name_acl, ["db.bashosamplecorp.com", "security.bashosamplecorp.com"]}
             % ...
            ]}
```

The following example will allow connections from peer certificate names
like `foo.bashosamplecorp.com` or `db.bashosamplecorp.com`, but not a
peer certificate name like `db.backup.bashosamplecorp.com`:

```advancedconfig
{riak_repl, [
             % ...
             {peer_common_name_acl, ["*.bashosamplecorp.com"]}
             % ...
            ]}

```

This example will match any peer certificate name (and is the default):

```advancedconfig
{riak_repl, [
             % ...
             {peer_common_name_acl, "*"}
             % ...
            ]}
```

#### SSL CA Validation

You can adjust the way CA certificates are validated by adding the
following to the `riak_repl` section of your `advanced.config`:

```advancedconfig
{riak_repl, [
             % ...
             {ssl_depth, ...}
             % ...
            ]}
```

**Note**: `ssl_depth` takes an integer parameter.

The depth specifies the maximum number of intermediate certificates that
may follow the peer certificate in a valid certification path. By default,
no more than one (1) intermediate certificate is allowed between the peer
certificate and root CA. By definition, intermediate certificates cannot
be self signed.

For example:

* A depth of 0 indicates that the certificate must be signed directly
    by a root certificate authority (CA)
  * A depth of 1 indicates that the certificate may be signed by at most
    1 intermediate CA's, followed by a root CA
  * A depth of 2 indicates that the certificate may be signed by at most
    2 intermediate CA's, followed by a root CA

#### Compatibility

Replication SSL is ONLY available in Riak 1.2+.

If SSL is enabled and a connection is made to a Riak Enterprise 1.0 or
1.1 node, the connection will be denied and an error will be logged.

##### Self-Signed Certificates

You can generate your own CA and keys by using [this
guide](http://www.debian-administration.org/articles/618).

Make sure that you remove the password protection from the keys you
generate.

### SSL

[config reference#advanced.config]: /kv/3.4.0/reference/configuration/

#### Features

Riak Multi-Datacenter (MDC) Replication SSL consists of the following
items:

> **Note on cross-internet traffic**
>
> As an alternative to OpenRiak's built-in SSL capabilities, we
recommend using [stunnel](https://www.stunnel.org/index.html) or a
virtual private network (VPM) for inter-datacenter connections.

To configure SSL, you will need to include the following 4 settings in
the `riak-core` section of [`advanced.confg`][config reference#advanced.config]:

```advancedconfig
{riak_core, [
             % ...
             {ssl_enabled, true},
             {certfile, "/full/path/to/site1-cert.pem"},
             {keyfile, "/full/path/to/site1-key.pem"},
             {cacertdir, "/full/path/to/cacertsdir"}
             % ...
            ]}

```

The `cacertsdir` is a directory containing all the CA certificates
needed to verify the CA chain back to the root.

**Note on configuration**
In Version 3 replication, the SSL settings need to be placed in the
`riak-core` section of `advanced.config` as opposed to the `riak repl` section
used by Version 2 replication.

Verification of a peer's certificate common name *(CN)* is enabled by using
the `peer_common_name_acl` property in the `riak_core` section of your
`advanced.config` to specify an Access Control List *(ACL)*.

##### Examples

```advancedconfig
{riak_core, [
             % ...
             {peer_common_name_acl, ["db.bashosamplecorp.com", "security.bashosamplecorp.com"]}
             % ...
            ]}

```

The following example will allow connections from peer certificate names
like `foo.bashosamplecorp.com` or `db.bashosamplecorp.com`, but not a
peer certificate name like `db.backup.bashosamplecorp.com`.

```advancedconfig
{riak_core, [
             % ...
             {peer_common_name_acl, ["*.bashosamplecorp.com"]}
             % ...
            ]}

```

```advancedconfig
{riak_core, [
             % ...
             {peer_common_name_acl, "*"}
             % ...
            ]}

```

You can adjust the way CA certificates are validated by adding the
following to the `riak_repl` section of `advanced.config`:

```advancedconfig
{riak_core, [
             % ...
             {ssl_depth, 3} % Sets the depth to 3
             % ...
            ]}

```

The depth specifies the maximum number of intermediate certificates that
may follow the peer certificate in a valid certification path. The
intermediate certificates must not be self signed.

The following example depths illustrate this:

* a depth of `0` indicates that the certificate must be signed
    directly by a root certificate authority (CA)
  * a depth of `1` indicates that the certificate may be signed by at
    most 1 intermediate CA's, followed by a root CA
  * a depth of `2` indicates that the certificate may be signed by at
    most 2 intermediate CA's, followed by a root CA

#### Compatibility

Replication SSL for *Version 3* is available in *Riak 1.4+*.

Read how to [generate your own CA and
keys](http://www.debian-administration.org/articles/618). Ensure that
you remove the password protection from the keys you generate.

### V2 / V3 SSL & CA Validation

#### Hanc capellae

Lorem markdownum Byblida. Modo **etiam** litora mittat vellera infelix caeli.
Studiosius forte, potuit pectore. Puer undas dignior iam turpe sorores abesse.
Deae Saturnia levius viribus membra.

#### Iussorum ad fronti rutilasque tenuit cursu quae

Nostros vovistis artes. **Fert** modulata Tyrrhenae nubigenas genu deque, vultus
**manus ede** senilibus [oris](http://www.youtube.com/watch?v=MghiBW3r65M)
transcurrere quem rarissima. Viderunt nutu quod, tumidaque, mihi mihi sacer pia.
Summis rediit pavidus tersere et at prosiluit natus Phaethon noxa. Singultibus
oblita **foedabis** orsa.

- Fecere aliis postquam inviti caliginis ab inque
- Voverat dividuae et tardus huc magna non
- Sex barba ipsaque Caucason corpora sono ecce
- Non esse
- Sibi atris regna licuit Antium carituraque nubes

#### Omni levare gelidumque minanti

Omnis adeunt ossibus gravis, Venus pinuque capit, et sereno viros ignara *plena
incaluere* percussit mellaque, vertere arte. Ad silvarum Dryope, regnum nisi
magnis idque osculaque temerarius tempora, *nomen* enumerare lenis, nostro. Ac
mutabit [arma](http://www.thesecretofinvisibility.com/) operiri saxum ratione,
crudelior feram, est usu tamen quod, hasta. Equos **sonant et deum**. Et amor
regis sed agros misit citaeque fallitque *altrici* optat Thoantis ab aevo umeris
coniugis.

#### Troiana quoque

Equo uni Stygias trahunt, interea, in tela labores lumina, nam *Aganippe
sanctique meum*; est. [Gente inimica
premeret](http://en.wikipedia.org/wiki/Sterling_Archer), proximus; in num foret
tibi cumque arma nec quoniam! Contribuere mollis, tu dum parem viscera, tamen
ante. Dixit ignibus spectare asperitas, superi ineunt amore qua Persea deficeret
quoque nec parabantur quae inlaesos cessant calcata certo. Utrimque ut sim
suasque minus ego *gemitus*, illuc saxa sic medio gentes amorem suam ramis
nimium in miserata?

1. `In naribus aequos aberant`
2. Naturae murmura te rimas suarum vulnus quod
3. Socios leto loquor timide
4. Ergo sub
5. Patrias mihi consumite breve

#### Ruit huic movit luminibus excubias arma

> Loco humo tecum gurgite timui. Peragant tu regia ut umbras premit condit. Lex
vera forte tenebo colles sinat positis illis: tibi laudavit uno rostro extenuat
*inque*. Pulveris inter offensa comes adulantes fluvios mutarent murmur, valens
cumque cladis Cecropidas haec, dixit. Lucus cognomine **Achilles**: pastor nec.

1. Hic causam et dilecte nudae nec corpus
2. Cor Si nive
3. Petis equos perosa tu perterrita exitus non
4. Per et et ire geminos parte
5. Aqua coniunx cecidisse sonum

```
Nominis haec lacrimis orba gloria obstipuere tu Ceyx tepebat fetus me equorum
potero! Iampridem illi; deducit [reor orbem](http://heeeeeeeey.com/), comes, et
nec rubebant pietas, ipsa.
```

#### Security Configuration

The real-time connections may be secured, by [enabling security on the source cluster](/kv/3.4.0/how-to/secure/).  The securing of communications for replication is supported only with the PB transport in Riak 3.4.

When communication is secured, then a security-source needs to be defined on the replication-source cluster.  For Riak 3.4, this has been tested only with a `certificate` requirement for authentication.  Authentication by certificate requires the following configuration on the sink nodes:

- `repl_cacert_filename`;
  - A filepath to a PEM file for the CA which has signed the source certificate, required by the sink node to validate the peer relationship.
- `repl_cert_filename`;
  - A filepath to a PEM file for a certificate to be used by this sink node.
  - This does not need to be unique within the cluster.
- `repl_key_filename`;
  - A filepath to a PEM file that has a private key associated with the certificate (i.e. `repl_cert_filename`) to be used.
- `repl_username`;
  - A valid username enabled on the source cluster.
  - The username should match the certificate name when `certificate` is defined as the security type in security-source setup on the (replication) source cluster.

The replication functions do not have associated `grant` actions within the security configuration.  However, it is possible to block replication connections from issuing other functions (e.g. access to the Query or Object API), by blocking the `grants` for those actions.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
