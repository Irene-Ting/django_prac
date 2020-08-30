release: python pystore/manage.py migrate
web: gunicorn --pythonpath pystore pystore.wsgi --log-file -