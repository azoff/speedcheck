FROM python:3-alpine

ARG SQLITE3_DB_PATH=/var/lib/sqlite3.db
ENV SQLITE3_DB_PATH=$SQLITE3_DB_PATH

RUN pip install speedtest-cli

ADD bin /usr/local/bin/