#!/bin/bash
mongod &
python3 manage.py migrate                  # Apply database migrations
python3 manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
# touch /srv/logs/gunicorn.log
# touch /srv/logs/access.log
# tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting server.
exec python3 manage.py runserver 0.0.0.0:8000