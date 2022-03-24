#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

uwsgi --module best_scarf.wsgi --socket :8000 --master --enable-threads