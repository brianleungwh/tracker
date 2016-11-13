from base import *

DEBUG = False
ALLOWED_HOSTS = ['camdog.pro', '*']
# SESSION_COOKIE_HTTPONLY = False
# CSRF_COOKIE_HTTPONLY = False

CELERYBEAT_SCHEDULE = {
    'update-trackers': {
        'task': 'api.update_trackers',
        'schedule': crontab(minute=0, hour='*/4'),
    },
}
