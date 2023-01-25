#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "==================="
echo "PostgreSQL started"
echo "==================="
# gunicorn -b 0.0.0.0:5000 manage:app
python3 /app/app.py