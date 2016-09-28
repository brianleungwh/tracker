import requests

from tracker.keys.mailgun_keys import MAILGUN_API_KEY

def send_confirmation_message(user_email, results_page_url, initial_listings):
    body = build_email_body_with(initial_listings)
    msg = 'Hi! Here are the current listings for {results_page_url} \n\n{body}'.format(results_page_url=results_page_url, body=body)
    return requests.post(
        'https://api.mailgun.net/v3/sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': 'Mailgun Sandbox <postmaster@sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org>',
            'to': user_email,
            'subject': 'Tracker Created!',
            'text': msg
        })

def send_email_for_new_or_updated_listings(user_email, results_page_url, new_or_updated_listings):
    body = build_email_body_with(new_or_updated_listings)
    msg = 'Hi! Here are the updated listings for {results_page_url} \n\n{body}'.format(results_page_url=results_page_url, body=body)
    return requests.post(
        'https://api.mailgun.net/v3/sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': 'Mailgun Sandbox <postmaster@sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org>',
            'to': user_email,
            'subject': 'Newly Created or Updated Listings',
            'text': msg
        })


def build_email_body_with(listings_data):
    l = []
    for listing_id, listing_data in listings_data.iteritems():
        print(listing_data)
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
