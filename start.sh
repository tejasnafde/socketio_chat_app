#!/bin/bash
set -o errexit  # Exit on error

# Install dependencies
poetry install --no-interaction

# Always run migrations (Render handles DB persistence)
flask db upgrade

# Start Gunicorn with socket.io worker
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}
