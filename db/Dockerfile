FROM alpine:3

RUN apk update && apk add sqlite

ARG SQLITE3_DB_PATH=/var/lib/sqlite3.db
ENV SQLITE3_DB_PATH=$SQLITE3_DB_PATH

ARG MIGRATIONS_PATH=/var/lib/migrations
ENV MIGRATIONS_PATH=$MIGRATIONS_PATH

ADD migrations $MIGRATIONS_PATH
ADD migrate.sh /usr/bin/migrate.sh

CMD ["migrate.sh"]
