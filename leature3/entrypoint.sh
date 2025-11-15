# create the file with the entrypoint we discussed
mkdir -p leature3
cat > leature3/entrypoint.sh <<'EOF'
#!/bin/sh
set -e

: "${PORT:=8000}"

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

exec gunicorn leature3.wsgi:application --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-30}
EOF

# make executable
git add leature3/entrypoint.sh
git commit -m "Add entrypoint script"
git push origin main   # or whatever branch Jenkins builds
