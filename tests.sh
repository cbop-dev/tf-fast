#!/bin/bash
. .venv/bin/activate && \
#pytest -vv tests

if [ $# -eq 0 ]; then
    pytest tests
else
    pytest "$@"
fi
