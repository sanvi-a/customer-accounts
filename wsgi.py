"""WSGI entry point: `flask --app wsgi run` or `gunicorn wsgi:app`."""
from accounts import create_app

app = create_app()
