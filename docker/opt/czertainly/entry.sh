#!/bin/sh

CPU_COUNT=$(getconf _NPROCESSORS_ONLN)   # honours the cgroup CPU quota
: "${GUNICORN_WORKERS:=${CPU_COUNT:-1}}"
: "${GUNICORN_THREADS:=${GUNICORN_THREADS:-4}}"

czertainlyHome="/opt/czertainly"
source ${czertainlyHome}/static-functions

log "INFO" "Launching PyADCS Connector"

cd /opt/czertainly
#python manage.py migrate
python migrate.py

exec gunicorn \
  --worker-class gthread \
  --workers "$GUNICORN_WORKERS" \
  --threads  "$GUNICORN_THREADS" \
  --timeout  600 \
  --bind     0.0.0.0:8080 \
  --worker-tmp-dir /dev/shm \
  CZERTAINLY_PyADCS_Connector.wsgi:application

#exec "$@"
