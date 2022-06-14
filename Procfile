web: gunicorn myserver.wsgi:application --log-file - --log-level debug
heroku config:set DISABLE_COLLECTSTATIC=1
python manage.py collectstatic --noinput
manage.py migrate