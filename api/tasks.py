from celery.decorators import task
from tracker import celery_app
from api.models import User, Tracker
from core_listing_scraper import get_current_listings, make_dict
from mailgun_email_api.mailgun_email_api import send_confirmation_message, send_email_for_new_or_updated_listings


@task(name='create_tracker')
def create_tracker(user_email, results_page_url):
    user, created = User.objects.get_or_create(email=user_email)
    user.save()
    data = get_current_listings(results_page_url)
    tracker = Tracker(user=user, results_page_url=results_page_url, listings=data)
    tracker.save()
    # send initial email with current listings
    send_confirmation_message(user_email, results_page_url, data)


@celery_app.task(name='api.update_trackers')
def update_trackers():
    users = User.objects.all()

    for user in users:

        trackers = user.tracker_set.all()

        for tracker in trackers:

            results_page_url = tracker.results_page_url

            outdated_listings = tracker.listings

            current_listings = get_current_listings(results_page_url)

            new_or_updated_listings = get_new_or_updated_listings(outdated_listings, current_listings)

            if new_or_updated_listings:

                send_email_for_new_or_updated_listings(user.email, results_page_url, new_or_updated_listings)

            tracker.listings = current_listings

            tracker.save()


def get_new_or_updated_listings(outdated_listings, current_listings):

    new_or_updated_listings = {}

    for craig_id, current_listing in current_listings.iteritems():

        outdated_listing = outdated_listings.get(craig_id)

        if listing_did_not_exist(outdated_listing):

            new_or_updated_listings[craig_id] = make_dict(current_listing)

        elif listing_has_been_updated(outdated_listing, current_listing):

            new_or_updated_listings[craig_id] = make_dict(current_listing)
            
        else:
            # listing has not changed
            continue

    return new_or_updated_listings



def listing_has_been_updated(outdated_listing, current_listing):
    has_been_updated = (outdated_listing.get('title') != current_listing.get('title') or
                        outdated_listing.get('price') != current_listing.get('price') or
                        outdated_listing.get('absolute_url') != current_listing.get('absolute_url') or
                        outdated_listing.get('last_modified_at') != current_listing.get('last_modified_at'))
    return has_been_updated

def listing_did_not_exist(outdated_listing):
    return outdated_listing == None
