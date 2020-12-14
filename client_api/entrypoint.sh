#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
uvicorn client_api.asgi:application --host=0.0.0.0 --port=7000 --reload