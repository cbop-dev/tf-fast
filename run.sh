#!/bin/bash
. .venv/bin/activate && \
#flask --app tffast run --debug
fastapi dev --port 5000 tffast/main.py
