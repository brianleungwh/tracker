import requests
from email_templates import *

from tracker.keys.mailgun_keys import MAILGUN_API_KEY

def send_confirmation_message(user_email, results_page_url, initial_listings):
    body = build_email_body_with(initial_listings)
    msg = CONFIRMATION_MSG.format(results_page_url=results_page_url, body=body)
    return requests.post(
        'https://api.mailgun.net/v3/tracking.camdog.pro/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': 'CamDog <mailgun@tracking.camdog.pro>',
            'to': user_email,
            'subject': 'Tracking Initiated For {url}'.format(url=results_page_url),
            'text': msg
        })

def send_email_for_new_or_updated_listings(user_email, results_page_url, new_or_updated_listings):
    body = build_email_body_with(new_or_updated_listings)
    msg = NEW_OR_UPDATED_LISTINGS_MSG.format(results_page_url=results_page_url, body=body)
    return requests.post(
        'https://api.mailgun.net/v3/tracking.camdog.pro/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': 'CamDog <mailgun@tracking.camdog.pro>',
            'to': user_email,
            'subject': 'New or Updated Listings Found For {url}'.format(url=results_page_url),
            'text': msg
        })


def build_email_body_with(listings_data):
    l = []
    for listing_id, listing_data in listings_data.iteritems():
        title = ''
        price = ''
        url = ''
        last_modified_at = ''

        if listing_data['title']:
            title = listing_data['title'].encode('utf-8')

        if listing_data['price']:
            price = listing_data['price'].encode('utf-8')

        if listing_data['absolute_url']:
            url = listing_data['absolute_url'].encode('utf-8')

        if listing_data['last_modified_at']:
            last_modified_at = listing_data['last_modified_at'].encode('utf-8')
        
        s = 'Title: {title}\nPrice: {price}\nURL: {url}\nLast Modified At: {last_modified_at}\n'.format(title=title, price=price, url=url, last_modified_at=last_modified_at)
        l.append(s)
    return '\n\n'.join(l)
