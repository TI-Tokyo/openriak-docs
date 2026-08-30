ARG NODE_VERSION=24
ARG HUGO_VERSION=0.165.0
FROM node:${NODE_VERSION}-alpine AS metadata
WORKDIR /project
COPY . .
RUN node tools/scripts/generate-version-mounts.js && node tools/scripts/sync-product-metadata.js

FROM ghcr.io/gohugoio/hugo:v${HUGO_VERSION} AS build
ARG INCLUDE_DRAFTS=true
ARG HUGO_BASEURL=https://www.openriak.org/docs/
WORKDIR /project
COPY --from=metadata --chown=1000:1000 /project /project
RUN HUGO_BASEURL="$HUGO_BASEURL" INCLUDE_DRAFTS="$INCLUDE_DRAFTS" sh ./tools/scripts/build.sh && \
    authority_and_path="${HUGO_BASEURL#*://}" && \
    case "$authority_and_path" in */*) base_path="${authority_and_path#*/}" ;; *) base_path="" ;; esac && \
    base_path="${base_path%/}" && \
    deploy_root="/project/deploy${base_path:+/$base_path}" && \
    mkdir -p "$deploy_root" && \
    cp -a public/. "$deploy_root/" && \
    if [ -f public/404.html ]; then cp public/404.html /project/deploy/404.html; fi

FROM nginx:1.29-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /project/deploy /usr/share/nginx/html
EXPOSE 80
