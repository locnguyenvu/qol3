FROM python:alpine

ARG TIMEZONE
WORKDIR /src

COPY setup.py .
RUN apk add --no-cache --virtual .build-deps g++ libffi-dev openssl-dev tzdata chromium
ENV TZ $TIMEZONE
RUN python -m pip install uWSGI && \
    python -m pip install -e . && \
    python -m pip install supervisor

COPY config.py .
COPY wsgi.py .
COPY qol3 ./qol3
COPY lang ./lang

COPY docker/crontab /var/spool/cron/crontabs/root
COPY docker/supervisor.d/ supervisor.d
COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/bin/sh", "-c", "/entrypoint.sh" ]
