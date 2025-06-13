#!/bin/bash
. .venv/bin/activate && \
#flask --app tffast run --debug
fastapi dev tffast/main.py
