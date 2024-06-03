#!/bin/sh

czertainlyHome="/opt/czertainly"
source ${czertainlyHome}/static-functions

log "INFO" "Launching PyADCS Connector"

cd /opt/czertainly
#python manage.py migrate
python migrate.py
exec gunicorn --bind '0.0.0.0:8080' --timeout 600 --worker-tmp-dir /dev/shm --workers "${GUNICORN_WORKERS:-3}" CZERTAINLY_PyADCS_Connector.wsgi:application

#exec "$@"