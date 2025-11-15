#!/bin/sh
set -e

# default port fallback
: "${PORT:=8000}"

# optional: simple retry loop for migrations (handles DB not-ready)
MAX_RETRIES=${MIGRATE_RETRIES:-10}
SLEEP_SECONDS=${MIGRATE_SLEEP:-3}

n=0
until [ "$n" -ge "$MAX_RETRIES" ]; do
  echo "Attempt $((n+1)) to run migrations..."
  if python manage.py migrate --noinput; then
    echo "Migrations successful."
    break
  fi
  n=$((n+1))
  echo "Migrations failed; sleeping ${SLEEP_SECONDS}s before retry..."
  sleep "${SLEEP_SECONDS}"
done

if [ "$n" -ge "$MAX_RETRIES" ]; then
  echo "Migrations failed after ${MAX_RETRIES} attempts — exiting with error."
  exit 1
fi

# Start gunicorn as PID 1 so it receives signals properly
exec gunicorn leature3.wsgi:application --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-30}
