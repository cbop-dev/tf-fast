import multiprocessing
import os

# --- App Entry Point ---
wsgi_app = "tffast.main:app"

# --- Environment Detection & Aliasing ---
# Define which strings count as "development" mode
DEV_ALIASES = {"dev", "development", "local"}
RAW_ENV = os.getenv("APP_ENV", "production").lower()
DEBUG = RAW_ENV in DEV_ALIASES
PORT = os.getenv("PORT", "5000")
# --- Network ---
bind = "0.0.0.0:"+PORT

# --- Worker Configuration ---
worker_class = "uvicorn.workers.UvicornWorker"

if DEBUG:
    workers = 1
    reload = True
    preload_app = True
    loglevel = "debug"
    print("Running in DEBUG mode...")
else:
    # Production defaults
    workers = 3
    reload = False
    preload_app = True
    loglevel = "info"

# --- Logging ---
accesslog = "-"
errorlog = "-"