from tracker import celery_app
from api.models import User, Tracker
from email_services.email_utils import send_email_for_new_or_updated_listings

import json
import subprocess

import redis
r = redis.StrictRedis(host='redis', port=6379, db=0)

PYTHON = 'python'
MAIN_SCRAPY_SCRIPT = 'core_listing_scraper/initiate_spider.py'

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

def get_current_listings(results_page_url):
    subprocess.call([PYTHON, MAIN_SCRAPY_SCRIPT, results_page_url])

    data = {}
    listings = json.loads(r.get(results_page_url), encoding='utf-8')
    for listing in listings:
            data[listing['craig_id']] = {
                'title': listing['title'],
                'price': listing['price'],
                'absolute_url': listing['absolute_url'],
                'last_modified_at': listing['last_modified_at']
            }
    return data

def get_new_or_updated_listings(outdated_listings, current_listings):

    new_or_updated_listings = {}

    for craig_id, current_listing in current_listings.iteritems():

        outdated_listing = outdated_listings.get(craig_id)

        if listing_did_not_exist(outdated_listing):
            new_or_updated_listings[current_listing['craig_id']] = {
                'title': current_listing['title'],
                'price': current_listing['price'],
                'absolute_url': current_listing['absolute_url'],
                'last_modified_at': current_listing['last_modified_at']
            }
        elif listing_has_been_updated(outdated_listing, current_listing):
            new_or_updated_listings[current_listing['craig_id']] = {
                'title': current_listing['title'],
                'price': current_listing['price'],
                'absolute_url': current_listing['absolute_url'],
                'last_modified_at': current_listing['last_modified_at']
            }
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
