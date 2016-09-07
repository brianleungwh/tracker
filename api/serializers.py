from rest_framework import serializers
from api.models import User, Tracker
from urlparse import urlparse

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
        user = User.objects.get_or_create(email=email)
        user.save()
        # initialize tracker with scrapy app?
        # send initial email with current listings
        # return 201
        tracker = Tracker(user=user, result_page_url=result_page_url, listings=JSON_DATA)
        tracker.save()
        


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
