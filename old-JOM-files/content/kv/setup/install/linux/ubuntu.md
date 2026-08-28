---
sidebar_position: 7
title: Installing On Ubuntu or Debian
sidebar_label: "Use Ubuntu"
date: 2025-09-19
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[beforeinstall]: #before-installing-openriak
[Installing]: #installing-openriak
[verify]: #next-steps---verifying-openriak-install
[verifying-installation]: : ../../setup/install/verify

## Installing OpenRiak KV on Ubuntu

This guide provides the steps for installing OpenRiak KV on the most recent version of Ubuntu/Debian.

## Installing OpenRiak

  1. From a terminal window download the OpenRiak package with the following:


    ```bash
      wget https://files.tiot.jp/riak/kv/3.2/3.2.5/ubuntu/noble64/riak_3.2.5-OTP25_amd64.deb
    ```


  2. In the same terminal window, to install the OpenRiak package run this and answer any prompts in the process:

    ```bash
      dpkg -i riak_3.2.5-OTP25_amd64.deb
    ```

  3. You should see as the last line this:

    ```
      Complete!
    ```

  If you see that message, OpenRiak has installed successfully.

  4. Confirm the install completed by running:

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
