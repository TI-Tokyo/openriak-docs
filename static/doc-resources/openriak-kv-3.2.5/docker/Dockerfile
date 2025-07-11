FROM alpine:3.21

RUN echo https://files.tiot.jp/alpine/v3.21/main >> /etc/apk/repositories
RUN wget http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O /etc/apk/keys/alpine@tiot.jp.rsa.pub
RUN apk update
RUN apk add bash dos2unix

RUN apk add riak=3.2.5.25-r1
RUN sed -i -e "s/^storage_backend = .*$/storage_backend = leveled/g" /etc/riak/riak.conf
RUN sed -i -e "s/^## ring_size = 64$/ring_size = 8/g" /etc/riak/riak.conf
RUN sed -i -e "s/^tictacaae_active = passive$/tictacaae_active = active/g" /etc/riak/riak.conf
RUN sed -i -e "s/^## tictacaae_storeheads = disabled$/tictacaae_storeheads = enabled/g" /etc/riak/riak.conf

EXPOSE 8098
EXPOSE 8087

COPY ./docker-entrypoint.sh /
RUN dos2unix /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["start-openriak"]
