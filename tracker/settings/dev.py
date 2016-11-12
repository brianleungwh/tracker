from base import *

# schedule celery beat task to run every minute for easy testing
CELERYBEAT_SCHEDULE = {
    'update-trackers': {
        'task': 'api.update_trackers',
        'schedule': crontab(minute='*/1'),
    },
}
