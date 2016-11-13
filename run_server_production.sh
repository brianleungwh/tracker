#!/bin/bash

touch /code/scrapy.log
python manage.py collectstatic --no-input
gunicorn tracker.wsgi --bind 0.0.0.0:8000
