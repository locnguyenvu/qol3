#!/usr/bin/env sh

CURRENT_DIR=$(pwd)

if [ ! -d "${CURRENT_DIR}/assets" ]; then
    mkdir "${CURRENT_DIR}/assets"
fi

/usr/local/bin/supervisord -c /etc/supervisord.conf
