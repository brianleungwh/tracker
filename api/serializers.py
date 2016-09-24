from rest_framework import serializers
from api.models import User, Tracker
from urlparse import urlparse

from core_listing_scraper.utils import *
from core_listing_scraper.spiders.listing_spider import ListingSpider
from email_services.email_utils import send_confirmation_message

import json
import subprocess

import redis
r = redis.StrictRedis(host='redis', port=6379, db=0)

PYTHON = 'python'
MAIN_SCRAPY_SCRIPT = 'core_listing_scraper/initiate_spider.py'

class UserTrackerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    results_page_url = serializers.URLField(required=True, max_length=500)

    def validate_email(self, email):
        return email

    def validate_results_page_url(self, results_page_url):
        # check this is in fact a craigslist result page url
        if not self._is_craigslist_url(results_page_url):
            raise serializers.ValidationError('Invalid URL')
        return results_page_url

    @staticmethod
    def _is_craigslist_url(url):
        parsed_url = urlparse(url)
        return ((parsed_url.scheme == 'http' or parsed_url.scheme == 'https') and
                parsed_url.netloc.split('.')[1] == 'craigslist' and 
                parsed_url.path.split('/')[1] == 'search')

    def extract_validated_data(self):
        email = self.validated_data['email']
        results_page_url = self.validated_data['results_page_url']
        return email, results_page_url

    def create_tracker(self):
        email, results_page_url = self.extract_validated_data()
        user, created = User.objects.get_or_create(email=email)
        user.save()
        subprocess.call([PYTHON, MAIN_SCRAPY_SCRIPT, results_page_url])
        data = self.read_data(results_page_url)
        tracker = Tracker(user=user, results_page_url=results_page_url, listings=data)
        tracker.save()
        # send initial email with current listings
        send_confirmation_message(email, results_page_url, data)

        
    @staticmethod
    def read_data(results_page_url):
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

    def tracker_does_not_already_exist(self):
        email, results_page_url = self.extract_validated_data()
        try:
            user = User.objects.get(email=email)
            if user.tracker_set.filter(results_page_url=results_page_url).exists():
                return False
            return True
        except User.DoesNotExist as E:
            return True


    def delete_tracker(self):
        if self.tracker_does_not_already_exist():
            return
        email, results_page_url = self.extract_validated_data()
        user = User.objects.get(email=email)
        user.tracker_set.get(results_page_url=results_page_url).delete()
