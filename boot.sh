#!/bin/bash
source venv/bin/activate
export FLASK_APP="app"

while true; do
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - app:app 