from tracker import celery_app

@celery_app.task(name='api.update_trackers')
def update_trackers():
    print('update_trackers called')
