#!/bin/sh

cd backend

python ./manage.py collectstatic --noinput
python ./manage.py wait_for_db
python ./manage.py makemigrations
python ./manage.py migrate

gunicorn core.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace above gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8000