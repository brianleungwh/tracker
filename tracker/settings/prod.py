from base import *


MAILGUN_API_ENDPOINT = 'https://api.mailgun.net/v3/tracking.camdog.pro/messages'
MAILGUN_DISPLAY_NAME = 'CamDog <mailgun@tracking.camdog.pro>'

DEBUG = False
ALLOWED_HOSTS = ['.camdog.pro']
# SESSION_COOKIE_HTTPONLY = False
# CSRF_COOKIE_HTTPONLY = False

CELERYBEAT_SCHEDULE = {
    'update-trackers': {
        'task': 'api.update_trackers',
        'schedule': crontab(minute=0, hour='*/4'),
    },
}
