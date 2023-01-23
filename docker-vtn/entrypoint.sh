#!/bin/sh
echo "======================="
echo "Waiting for postgres..."
echo "======================="
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "======================="
echo "PostgreSQL started"
echo "======================="
nodemon --watch /app --watch /openleadr-python \
            --exec python3 /app/app.py
# python3 /app/app.py
# gunicorn -b 0.0.0.0:5000 manage:app