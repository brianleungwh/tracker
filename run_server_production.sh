#!/bin/bash

python manage.py collectstatic
gunicorn tracker.wsgi --bind 0.0.0.0:8000
