#!/bin/bash
. .venv/bin/activate && \
#flask --app tffast run --debug
#fastapi dev --port 5000 tffast/main.py
APP_ENV=dev gunicorn -c gunicorn_conf.py
