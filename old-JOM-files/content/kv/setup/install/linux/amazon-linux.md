---
sidebar_position: 2
title:Installing On AWS Amazon Linux
sidebar_label: "Use Amazon Linux"
date: 2025-09-16
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[install]: #installing-on-amazon-linux
[next steps]: #next-steps---verifying-openriak-install

[verifying-installation]: : ../../setup/install/verify

## Installing OpenRiak KV on Amazon Linux

This guide provides the steps for installing OpenRiak KV on the most recent version of Amazon Linux.

## Installing on Amazon Linux

>[!NOTE]Note on AWS instances
>This tutorial assumes you have an already configured basic AWS EC2 instance running Amazon Linux.

    1. From the command line download OpenRiak with the following:
    itself.

        ```
            wget "https://files.tiot.jp/riak/kv/3.4/3.4.0/amazon/2023%20(x86_64)/riak-3.4.0.OTP26-1.amzn2023.x86_64.rpm"
        ```

    >[!NOTE]Note on quoting the URL
    >The quotations around the URL are essential to prevent an error relating to the use of () in the URL

    2. Next, install the package with:

        ```
            sudo rpm -i --nodeps riak-3.2.6.OTP24-1.amzn2023.x86_64.rpm
        ```
     >[!NOTE]Note on the use of the --nodeps flag
    >The use of the `--nodeps` flag allows to

    3. Confirm the install completed by running:

        ```bash
            riak
        ```

  You should see this as the result:

    ```bash
      $riak

      Usage: riak [COMMAND] [ARGS]

      Commands:

        foreground              Start release with output to stdout
        remote_console          Connect remote shell to running node
        rpc [Mod [Fun [Args]]]] Run apply(Mod, Fun, Args) on running node
        eval [Exprs]            Run expressions on running node
        stop                    Stop the running node
        restart                 Restart the applications but not the VM
        reboot                  Reboot the entire VM
        pid                     Print the PID of the OS process
        ping                    Print pong if the node is alive
        console                 Start the release with an interactive shell
        console_clean           Start an interactive shell without the release's applications
        console_boot [File]     Start an interactive shell for boot script [File]
        daemon                  Start release in the background with run_erl (named pipes)
        daemon_boot [File]      Start boot script [File] in the background with run_erl (named pipes)
        daemon_attach           Connect to node started as daemon with to_erl (named pipes)
        upgrade [Version]       Upgrade the running release to a new version
        downgrade [Version]     Downgrade the running release to a new version
        install [Version]       Install a release
        uninstall [Version]     Uninstall a release
        unpack [Version]        Unpack a release tarball
        versions                Print versions of the release available
        escript                 Run an escript in the same environment as the release
        status                  Verify node is running and then run status hook scripts
        admin|repl|debug|chkconfig
    ```

## Next steps - Verifying OpenRiak install

Once the node has been installed, we recommend verifying the node is able to start and respond to requests by following the steps [here](: ../../setup/install/verifyying-installation).