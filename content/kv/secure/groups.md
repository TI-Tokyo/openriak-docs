---
title: Groups
sidebar_label: "Groups"
date: 2026-01-13
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[overview]: #overview
[Create group]: #creating-a-group
[Managing group]: #managing-groups

# Overview

This section covers group management for OpenRiak security, the following pages cover other sections of OpenRiak security:

    1. [Basics](: ../../configure/secure/basics)
    2. [Networking](: ../../configure/secure/networking)
    3. [Users](: ../../configure/secure/users)
    4. [Sources](: ../../configure/secure/security-sources)

Groups within OpenRiak Security allow for easy management of permissions for multiple users at once, without having to make the changes individually.

# Creating a group

You can create a group with the following command:

    ```bash
        riak admin security add-group <groupname>
    ```

In the following example, we are making a group called "admin":

    ```bash
        riak admin security alter-user riakuser groups=admin
        ok
    ```

This producdes the following output:

    ```bash
        +----------+---------------+----------------------------------------+------------------------------+
        | username |   member of   |                password                |           options            |
        +----------+---------------+----------------------------------------+------------------------------+
        | riakuser |     admin     |269fcd0c4d1ee2115c588f64ab47252bd5eefe4a|              []              |
        +----------+---------------+----------------------------------------+------------------------------+
    ```

# Managing groups

There are a number of actions that can be taken again groups including: add a user, remove a user or group, add a group to another group.

## Adding a user to a group

The following example shows how to add a user (called riakuser in this case) to an existing group (admin).

    ```bash
        riak admin security alter-user riakuser groups=admin
    ```

The response from the system should appear similar to the following:

    ```bash
        +----------+---------------+----------------------------------------+------------------------------+
        | username |   member of   |                password                |           options            |
        +----------+---------------+----------------------------------------+------------------------------+
        | riakuser |     admin     |269fcd0c4d1ee2115c588f64ab47252bd5eefe4a|              []              |
        +----------+---------------+----------------------------------------+------------------------------+
    ```
You should always check that the correct user has been added to the correct group.

If we’d like to make the user riakuser a member of both admin and user groups:

    ```bash
        riak admin security alter-user riakuser groups=admin,dev
        ok

        +----------+---------------+----------------------------------------+------------------------------+
     username |   member of   |                password                |           options            |
        +----------+---------------+----------------------------------------+------------------------------+
     riakuser |  dev, admin   |269fcd0c4d1ee2115c588f64ab47252bd5eefe4a|              []              |
        +----------+---------------+----------------------------------------+------------------------------+

        ok
    ```

There is no way to incrementally add groups; even if `riakuser` was already an admin, it is necessary to list it again when adding the dev group. Instead, when you want to remove a group from a user, use alter-user and list all other groups as seen below.

## Adding a group to another group

Groups can be added to other groups in order to allow for incremental permissions.

The following command adds the `admin` group to the `dev` group:

    ```bash
        riak admin security alter-group admin groups=dev

        +----------+---------------+------------------------------+
        |  group   |   member of   |           options            |
        +----------+---------------+------------------------------+
        |  admin   |      dev      |              []              |
        +----------+---------------+------------------------------+

        ok
    ```

## Deleting a user or group

To delete a group, use the `del-user` command:

    ```bash
        riak admin security del-user riakuser
    ```

You should seen an output similar to below:

    ```bash
        Successfully deleted riakuser
        ok
    ```

To delete a group, use the `del-group` command:

    ```bash
        riak admin security del-group admin
    ```

This produces the following output:

    ```bash
        Successfully deleted admin
        ok
    ```

>[!NOTE]Note on adding/deleting multiple users
>The riak admin security command does not currently allow you to add or delete multiple users using a single command. Instead, they must be added or deleted one by one.