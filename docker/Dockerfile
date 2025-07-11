FROM node:alpine

LABEL org.opencontainers.image.title="OpenRiak Docs" \
      org.opencontainers.image.description="Builds the OpenRiak documentation based on the source code and static content files." \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.authors="OpenRiak <docs@openriak.org>" \
      org.opencontainers.image.url="https://www.openriak.com/docs" \
      org.opencontainers.image.documentation="https://www.openriak.com/docs" \
      org.opencontainers.image.source="https://github.com/openrial/openriak-docs" \
      org.opencontainers.image.revision="main" \
      org.opencontainers.image.licenses="Apache 2.0"

RUN echo "fs.file-max = 65535" >> /etc/sysctl.conf
RUN sysctl -p

RUN npm install -g npm@latest
RUN npm config set update-notifier false

EXPOSE 3000 9229
