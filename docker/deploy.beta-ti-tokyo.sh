#!/usr/bin/env bash

set -euo pipefail

git pull

rm -rf build docker-wip public

HUGO_BASEURL="https://www.tiot.jp/openriak-docs-beta/" \
INCLUDE_DRAFTS=true \
./docker/build.static.sh release

rsync -avz \
    --progress \
    --delete-before \
    public/ \
    peter-clark@www.tiot.jp:/var/www/www-tiot-jp-2025-03-29/openriak-docs-beta/
