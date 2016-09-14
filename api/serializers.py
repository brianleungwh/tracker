from rest_framework import serializers
from api.models import User, Tracker
from urlparse import urlparse

from core_listing_scraper.utils import *
from core_listing_scraper.spiders.listing_spider import ListingSpider
from core_listing_scraper.pipelines import DATA_FILE

import subprocess
import pandas as pd

PYTHON = 'python'
MAIN_SCRAPY_SCRIPT = 'core_listing_scraper/scrape_to_file.py'

class UserTrackerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    result_page_url = serializers.URLField(required=True, max_length=500)

    def validate_email(self, email):
        return email

    def validate_result_page_url(self, result_page_url):
        # check this is in fact a craigslist result page url
        if not self._is_craigslist_url(result_page_url):
            raise serializers.ValidationError('Invalid URL')
        return result_page_url

    @staticmethod
    def _is_craigslist_url(url):
        parsed_url = urlparse(url)
        return ((parsed_url.scheme == 'http' or parsed_url.scheme == 'https') and
                parsed_url.netloc.split('.')[1] == 'craigslist' and 
                parsed_url.path.split('/')[1] == 'search')

    def extract_validated_data(self):
        email = self.validated_data['email']
        result_page_url = self.validated_data['result_page_url']
        return email, result_page_url

    def create_tracker(self):
        email, result_page_url = self.extract_validated_data()
        user, created = User.objects.get_or_create(email=email)
        user.save()
        # return 201
        subprocess.call([PYTHON, MAIN_SCRAPY_SCRIPT, result_page_url])
        data = self.read_data_from_data_file()
        print(data)
        tracker = Tracker(user=user, result_page_url=result_page_url, listings=data)
        tracker.save()
        # send initial email with current listings

        
    @staticmethod
    def read_data_from_data_file():
        df = pd.read_csv(DATA_FILE)
        # http://pandas.pydata.org/pandas-docs/stable/missing_data.html#filling-missing-values-fillna
        df = df.fillna('')
        # http://stackoverflow.com/questions/26716616/convert-pandas-dataframe-to-dictionary
        df.set_index('craig_id', drop=True, inplace=True)
        return df.to_dict(orient='index')
            


    def tracker_does_not_already_exist(self):
        email, result_page_url = self.extract_validated_data()
        try:
            user = User.objects.get(email=email)
            if user.tracker_set.filter(result_page_url=result_page_url).exists():
                return False
            return True
        except User.DoesNotExist as E:
            return True


    def delete_tracker(self):
        print('deleting tracker')
        print(self.validated_data)
