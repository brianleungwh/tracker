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


def build_email_body_with(listings_data):
    l = []
    for listing_id, listing_data in listings_data.iteritems():
        print(listing_data)
        title = listing_data['title']
        price = listing_data['price']
        url = listing_data['absolute_url']
        s = 'Title: {title}\nPrice: {price}\nURL: {url}'.format(title=title, price=price, url=url)
        l.append(s)
    return '\n\n'.join(l)
