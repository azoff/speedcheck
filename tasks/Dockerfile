FROM python:3-alpine

ARG SQLITE3_DB_PATH=/var/lib/sqlite3.db
ENV SQLITE3_DB_PATH=$SQLITE3_DB_PATH

ARG SECRETS_PATH=/run/secrets/speedcheck/secrets.json
ENV SECRETS_PATH=$SECRETS_PATH

RUN pip install speedtest-cli python-twitter

ADD bin /usr/local/bin/