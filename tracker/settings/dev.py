from base import *


MAILGUN_API_ENDPOINT = 'https://api.mailgun.net/v3/sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org/messages'
MAILGUN_DISPLAY_NAME = 'Mailgun Sandbox <postmaster@sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org>'

# schedule celery beat task to run every minute for easy testing
CELERYBEAT_SCHEDULE = {
    'update-trackers': {
        'task': 'api.update_trackers',
        'schedule': crontab(minute='*/1'),
    },
}
