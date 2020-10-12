#!/bin/sh
python manage.py migrate --noinput
uwsgi --ini /app/config/server/uwsgi.ini