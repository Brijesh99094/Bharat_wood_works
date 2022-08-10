release: python manage.py migrate
heroku ps:scale web=1
web: gunicorn Bww_v1.wsgi --log-file -
