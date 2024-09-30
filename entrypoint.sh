#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn --workers=2 --bind 0.0.0.0:8000 kittens.wsgi