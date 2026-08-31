ARG NODE_VERSION=24
ARG HUGO_VERSION=0.165.0

# Product changes invalidate this stage, but do not invalidate archive-build.
FROM node:${NODE_VERSION}-alpine AS core-metadata
ARG CORE_BUILD_PROFILE=release
ARG RIAK_KV_VERSION=3.2.5
WORKDIR /project
COPY .hugo-version ./
COPY tools ./tools
COPY content/hugo.yaml ./content/hugo.yaml
COPY content/homepage ./content/homepage
COPY content/community ./content/community
COPY content/riak-kv ./content/riak-kv
COPY content/openriak-kv ./content/openriak-kv
COPY content/openriak-cs ./content/openriak-cs
COPY content/openriak-ts ./content/openriak-ts
COPY content/static ./content/static
COPY layouts/homepage ./layouts/homepage
COPY layouts/docs-theme ./layouts/docs-theme
COPY layouts/common-docs ./layouts/common-docs
RUN case "$CORE_BUILD_PROFILE" in \
      development) \
        node tools/scripts/generate-version-mounts.js \
          --base-config /project/content/hugo.yaml \
          --output /project/tools/generated/hugo.yaml \
          --include-version "riak-kv=$RIAK_KV_VERSION" && \
        node tools/scripts/sync-product-metadata.js \
          --include-version "riak-kv=$RIAK_KV_VERSION" ;; \
      beta-test|release) \
        node tools/scripts/generate-version-mounts.js \
          --base-config /project/content/hugo.yaml \
          --output /project/tools/generated/hugo.yaml && \
        node tools/scripts/sync-product-metadata.js ;; \
      *) echo "Unknown core build profile: $CORE_BUILD_PROFILE" >&2; exit 2 ;; \
    esac

FROM ghcr.io/gohugoio/hugo:v${HUGO_VERSION} AS core-build
ARG INCLUDE_DRAFTS=true
ARG HUGO_BASEURL=https://www.openriak.org/docs/
WORKDIR /project
COPY --from=core-metadata --chown=1000:1000 /project /project
RUN drafts=''; if [ "$INCLUDE_DRAFTS" = true ]; then drafts=--buildDrafts; fi; \
    hugo --source=/project/content --config=/project/tools/generated/hugo.yaml \
      --destination=/project/public --baseURL="$HUGO_BASEURL" --gc --minify \
      --panicOnWarning --noBuildLock --cleanDestinationDir $drafts

# Development and beta-test artifacts contain the core project only.
FROM scratch AS core-static
COPY --from=core-build /project/public/ /

# This stage only depends on archive content and the templates shared with it.
# Product documentation changes therefore reuse its cached result.
FROM ghcr.io/gohugoio/hugo:v${HUGO_VERSION} AS archive-build
ARG INCLUDE_DRAFTS=true
ARG HUGO_BASEURL=https://www.openriak.org/docs/
WORKDIR /project
COPY .hugo-version ./
COPY content/hugo-archives.yaml ./content/hugo-archives.yaml
COPY content/archive-technical-blog ./content/archive-technical-blog
COPY content/archive-mailing-list ./content/archive-mailing-list
COPY layouts/archive-technical-blog ./layouts/archive-technical-blog
COPY layouts/archive-mailing-list ./layouts/archive-mailing-list
COPY layouts/common-docs/data ./layouts/common-docs/data
COPY layouts/common-docs/layouts ./layouts/common-docs/layouts
COPY layouts/docs-theme/layouts/_default/section.search.json.json ./layouts/docs-theme/layouts/_default/section.search.json.json
RUN drafts=''; if [ "$INCLUDE_DRAFTS" = true ]; then drafts=--buildDrafts; fi; \
    hugo --source=/project/content --config=/project/content/hugo-archives.yaml \
      --destination=/project/public --baseURL="$HUGO_BASEURL" --gc --minify \
      --panicOnWarning --noBuildLock --cleanDestinationDir $drafts

FROM alpine:3.22 AS assembled
WORKDIR /project
COPY tools/scripts/assemble-site.sh /usr/local/bin/assemble-site
COPY --from=core-build /project/public /project/core
COPY --from=archive-build /project/public /project/archives
RUN sh /usr/local/bin/assemble-site /project/core /project/archives /project/public

# Build this target with --output to obtain one directory suitable for rsync.
FROM scratch AS static
COPY --from=assembled /project/public/ /

# The runtime image retains the existing /docs/ deployment prefix.
FROM alpine:3.22 AS deploy
ARG HUGO_BASEURL=https://www.openriak.org/docs/
WORKDIR /project
COPY --from=assembled /project/public /project/public
RUN authority_and_path="${HUGO_BASEURL#*://}"; \
    case "$authority_and_path" in */*) base_path="${authority_and_path#*/}" ;; *) base_path='' ;; esac; \
    base_path="${base_path%/}"; \
    deploy_root="/project/deploy${base_path:+/$base_path}"; \
    mkdir -p "$deploy_root"; \
    cp -a /project/public/. "$deploy_root/"; \
    if [ -f /project/public/404.html ]; then cp /project/public/404.html /project/deploy/404.html; fi

FROM nginx:1.29-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=deploy /project/deploy /usr/share/nginx/html
EXPOSE 80
