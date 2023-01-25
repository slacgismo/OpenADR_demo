#!/bin/sh

echo "Waiting for VTN..."

while ! nc -z vtn 8080; do
  sleep 0.1
done
echo "==================="
echo "VTN started"
echo "==================="
# gunicorn -b 0.0.0.0:5000 manage:app
python3 /app/app.py