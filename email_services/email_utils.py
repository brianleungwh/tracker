import requests

from tracker.keys.mailgun_keys import MAILGUN_API_KEY

def send_confirmation_message(user_email):
    return requests.post(
        'https://api.mailgun.net/v3/sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': 'Mailgun Sandbox <postmaster@sandboxb7fd6d2e0f5d451fa9931e2d775cedc1.mailgun.org>',
            'to': user_email,
            'subject': 'Tracker Created!',
            'text': 'Hi! Here are your listings \n <a>www.google.com</a>'
        })
