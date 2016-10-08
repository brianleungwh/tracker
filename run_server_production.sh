#!/bin/bash

python manage.py collectstatic --settings=tracker.settings.prod
gunicorn tracker.wsgi --bind 0.0.0.0:8000
