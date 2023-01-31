#!/bin/sh
db_host="${DB_HOST:-mysql}"
db_port="${DB_PORT:-3306}"
# echo "Waiting for $db_host..."
echo "DB_HOST $DB_HOST"
echo "DB_PORT $DB_PORT"


while ! nc -z $db_host $db_port; do
  sleep 0.2
done
echo "==================="
echo "$db_host started"
echo "==================="

# # gunicorn -b 0.0.0.0:5000 manage:app
python3 /app/app.py