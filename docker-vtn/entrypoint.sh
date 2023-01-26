#!/bin/sh
db_host="${DB_HOST:-postgres}"
echo "Waiting for $db_host..."
echo "DB_HOST $DB_HOST"


# while ! nc -z $db_host 5432; do
#   sleep 0.1
# done
# echo "==================="
# echo "$db_host started"
# echo "==================="

# # # gunicorn -b 0.0.0.0:5000 manage:app
# python3 /app/app.py