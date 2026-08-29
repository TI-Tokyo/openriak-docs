ARG HUGO_VERSION=0.165.0
FROM ghcr.io/gohugoio/hugo:v${HUGO_VERSION} AS build
ARG INCLUDE_DRAFTS=true
ARG HUGO_BASEURL=https://www.openriak.org/docs/
WORKDIR /project
COPY . .
RUN if [ "$INCLUDE_DRAFTS" = "true" ]; then hugo --gc --minify --noBuildLock --buildDrafts --baseURL "$HUGO_BASEURL"; else hugo --gc --minify --noBuildLock --baseURL "$HUGO_BASEURL"; fi && \
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
