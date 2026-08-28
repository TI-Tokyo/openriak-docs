---
sidebar_position: 1
title: Quick Start using Docker
sidebar_label: "Use Docker"
date: 2025-09-16
---

TODO: this was copied from quick start and needs enormous cleanups!

[setup-using-docker]: ../../setup/install/docker
[docker]: https://www.docker.com/
[leveled]: ../../configure/guides/backends/configure-leveled

## A Dev Node in under 5 mins!

This Quick Start guide is aimed at getting a local single-node cluster of OpenRiak KV for local testing and development.

A comprehensive guide for using Docker to run a full OpenRiak KV cluster is available at [Setup using Docker][setup-using-docker].

## Assumptions

    1. You have [Docker][docker] installed and have the neccessary permissions to run it.
    2. You want a single local node for testing and development purposes only.
    3. You don't mind if data is lost when instances are stopped.
    4. You want as small a footprint as possible.
    5. You want the same features as a full OpenRiak KV cluster.

## Settings

    1. We will use Alpine Linux 3.21 as our operating system.
    2. We will use OpenRiak KV version 3.2.5.
    2. We will use [Leveled][leveled] as our backend.
    2. We will turn on the TicTac Active Anti-Entropy (TicTac AAE) feature.
    3. We will turn on the Store Heads feature.
    4. We will make both Web (HTTP) and Protocol Buffer API interfaces available.
    5. We will only have 8 partitions.
    6. We will listen on `127.0.0.1` on the default ports (`8098` for web and `8087` for Protocol Buffers).

## Make your own Docker Image

    1. Create a file called `Dockerfile` with the following content:
        ```Dockerfile
        FROM alpine:3.21

        RUN echo https://files.tiot.jp/alpine/v3.21/main >> /etc/apk/repositories
        RUN wget http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O /etc/apk/keys/alpine@tiot.jp.rsa.pub
        RUN apk update

        RUN apk add riak=3.2.5.25-r1
        RUN sed -i -e "s/^storage_backend = .*$/storage_backend = leveled/g" /etc/riak/riak.conf
        RUN sed -i -e "s/^## ring_size = 64$/ring_size = 8/g" /etc/riak/riak.conf
        RUN sed -i -e "s/^tictacaae_active = passive$/tictacaae_active = active/g" /etc/riak/riak.conf
        RUN sed -i -e "s/^## tictacaae_storeheads = disabled$/tictacaae_storeheads = enabled/g" /etc/riak/riak.conf

        EXPOSE 8098
        EXPOSE 8087

        COPY ./docker-entrypoint.sh /
        ENTRYPOINT ["/docker-entrypoint.sh"]
        CMD ["riak daemon"]
        ```

    2. Create the startup script called `docker-entrypoint.sh`:
         ```
        #!/bin/bash
        set -e

        if [ "$1" = 'openriak' ]; then
            shift 1
            exec riak "$@"
        else
            exec "$@"
        fi
        ```
    3. Run `docker build -t openriak-kv .`.

## Start the OpenRiak KV instance

We will use the container name `openriak-kv` instead of a randomly generated name to make it easier to run commands.

Run:

    ```bash
        docker run -d --name openriak-kv openriak-kv
    ```

If you would like to check the container output, you can use `docker logs` like so:

    ```bash
    docker logs --follow openriak-kv
    ```

Press `Ctrl-q` to exit the logs.

## Send OpenRiak a command

Let's run the standard OpenRiak KV test:

    ```
    docker exec -it openriak-kv riak admin test
    ```

You should see a response similar to this:

    ```
    Successfully completed 1 read/write cycle to 'riak@127.0.0.1'
    ```

## Stop the container

    1. Run `docker container stop openriak-kv`

## Re-start the container

    1. Run `docker start -d openriak-kv`

## Clean up removing the container entirely

    1. Remove the container with `docker container rm openriak-kv`
    2. Remove the image `docker image rm openriak-kv`

