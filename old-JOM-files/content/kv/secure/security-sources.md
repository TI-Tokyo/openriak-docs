---
title: Security sources
sidebar_label: "Sources"
date: 2026-01-15
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[Overview]: #overview
[Trust]: #trust-based-authentication
[Managing group]: #managing-groups

# Overview

This section provides information on the available authentication sources for OpenRiak Security: trusted networks, password, pluggable authentication modules (PAM), and certificates.
These sources are represented as: trust, password, pam, and certificate in the `riak admin security` interface.

>![NOTE]Note on values used in these examples
>The examples below will assume that the network in question is `127.0.0.1/32` and that a OpenRiak user named `riakuser` has been created and that security has been enabled.

>![NOTE] Note on SSL connections
>If you use any of the aforementioned security sources, even trust, you will need to do so via a secure SSL connection.

# Trust-based Authentication

This form of authentication enables you to specify trusted CIDRs from which all clients will be authenticated by default.

    ```
        riak admin security add-source all 127.0.0.1/32 trust
    ```

This will produce the following output:

    ```
        Successfully added source
        ok
    ```

In the above example, we are specifying that anyone connecting to OpenRiak from the designated CIDR (`localhost` in this example) will be successfully authenticated.