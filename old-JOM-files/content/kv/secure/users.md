---
title: User Management
sidebar_label: "User management"
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

[overview]: #overview
[Add or remove user]: #adding-or-removing-a-user
[Changing characteristics]: #adding-and-modifying-user-characteristics


# Overview
This section covers Users with OpenRiak security. There are pages for Security Basics, Groups, Source management and Networking available from below:

1. [Basics](: ../../configure/secure/basics)
2. [Networking](: ../../configure/secure/networking)
3. [Groups](: ../../configure/secure/groups)
4. [Sources](: ../../configure/secure/security-sources)

OpenRiak security provides you with the ability to control authorisation by creating, modifying and deleting user characteristics while granting/revoking users selective access to OpenRiak functionality. 
You can assign one or more of the following characteristics:

    1. `username` - The defined username.
    2. `groups` - The "group" the user is part of, which allows specific permissions assigned to a range of users.
    3. `password` - authentication for the user.

>![NOTE]Note on characteristic changes after user creation
>The `username` is the one user characteristic that cannot be changed once a user has been created.

# Adding or Removing a User

## Add a user

To create a user with the username `riakuser`, we use the `add-user` command:

    ```bash
        riak admin security add-user riakuser
    ```

You should see a successful output such as:

    ```bash
        ok

        +----------+---------------+----------------------------------------+------------------------------+
        | username |   member of   |                password                |           options            |
        +----------+---------------+----------------------------------------+------------------------------+
        | riakuser |               |                                        |              []              |
        +----------+---------------+----------------------------------------+------------------------------+
    ```

This creates a user called `riakuser`, without any characteristics assigned to it except the `username` characteristic, which is the only one that must be assigned on creation.
You can also assign other characteristics at the same time, such as a password with:

    ```
        riak admin security add-user riakuser password=Test1234
    ```

## Removing a user

To remove a user, you can use the `del-user` command:

    ```bash
        riak admin security del-user riakuser
    ```

This command should produce:

    ```bash
        Successfully deleted riakuser
        ok
    ```

# Adding and modifying User Characteristics

Users characteristics can be set when the user is created, or it can be adding/changed after the fact with the `alter-user` command. 
In the following example, we are using the `alter-user` command to set the password of a user.

    ```bash
        riak admin security alter-user riakuser password=opensesame
    ```

This produces the following output:

    ```bash
        ok

        +----------+---------------+----------------------------------------+------------------------------+
        | username |   member of   |                password                |           options            |
        +----------+---------------+----------------------------------------+------------------------------+
        | riakuser |               |df3c07715213e0b4c28a78cbf5e08f12984d38b1|              []              |
        +----------+---------------+----------------------------------------+------------------------------+

        ok
    ```

When creating or altering a user, any number of `<option>=<value>` pairs can be appended to the end of the command. Any non-standard options will be stored and displayed via the `riak admin security print-users` command.

In the example below, we've added the favourite colour, the age and the favourite car of the user:

    ```bash
        riak admin security alter-user riakuser fav_car=mustang age=47 fav_color=red
        ok

        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | username |   member of   |                password                |                        options                         |
        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | riakuser |               |df3c07715213e0b4c28a78cbf5e08f12984d38b1|[{"age","47"},{"fav_car","mustang"},{"fav_color","red"}]|
        +----------+---------------+----------------------------------------+--------------------------------------------------------+

        ok
    ```
>![NOTE]
> Usernames cannot be changed using the `alter-user` command. For example, running `riak admin security alter-user riakuser username=other-name`, will instead add the `{"username","other-name"}` tuple to riakuser’s options.

You can check the characteristics and options of users with the `print-users` command:

    ```bash
        riak admin security print-users

        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | username |   member of   |                password                |                        options                         |
        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | riakuser |               |df3c07715213e0b4c28a78cbf5e08f12984d38b1|[{"age","47"},{"fav_car","mustang"},{"fav_color","red"}]|
        +----------+---------------+----------------------------------------+--------------------------------------------------------+
    ```

# Managing a user's groups

Groups are used to manage multiple users permissions at once without having to change/track the individual users.

## Adding a user to a group

You can assign a user to a group using the `group` option of the `alter-user` command as follows:

    ```bash
        riak admin security alter-user riakuser groups=dev
    ```

This produces the following output:
    ```bash
        ok

        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | username |   member of   |                password                |                        options                         |
        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | riakuser |      dev      |df3c07715213e0b4c28a78cbf5e08f12984d38b1|[{"age","47"},{"fav_car","mustang"},{"fav_color","red"}]|
        +----------+---------------+----------------------------------------+--------------------------------------------------------+

        ok
    ```
From the output above, you can see that we've added our existed user `riakuser` to the `dev` group.
There is no way to incrementally add groups. Even if a user is already a member of the `dev` group, it is necessary to list it again when adding to another group. 

## Removing a user from a group

If you want to remove a user from a group, you need to use the `alter-user` command and list all other groups the user is part of and omit the group(s) you wish to remove them from.
If you wish to remove them from all groups, use the `groups=` option with no list following such as below:

    ```bash
        riak admin security alter-user riakuser groups=
    ```

This will produce the following output:

    ```bash
        ok

        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | username |   member of   |                password                |                        options                         |
        +----------+---------------+----------------------------------------+--------------------------------------------------------+
        | riakuser |               |df3c07715213e0b4c28a78cbf5e08f12984d38b1|[{"age","47"},{"fav_car","mustang"},{"fav_color","red"}]|
        +----------+---------------+----------------------------------------+--------------------------------------------------------+

        ok
    ```
