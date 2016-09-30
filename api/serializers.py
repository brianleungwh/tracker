from rest_framework import serializers
from api.models import User, Tracker
from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs
from mailgun_email_api.mailgun_email_api import send_confirmation_message
from core_listing_scraper import get_current_listings


class UserTrackerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    results_page_url = serializers.URLField(required=True, max_length=500)

    def validate_email(self, email):
        return email

    def validate_results_page_url(self, results_page_url):
        # check this is in fact a craigslist result page url
        if not self._is_craigslist_url(results_page_url):
            raise serializers.ValidationError('Invalid URL')
        results_page_url = self.remove_pagination_query_if_exists(results_page_url)
        return results_page_url

    @staticmethod
    def _is_craigslist_url(url):
        parsed_url = urlparse(url)
        return ((parsed_url.scheme == 'http' or parsed_url.scheme == 'https') and
                parsed_url.netloc.split('.')[1] == 'craigslist' and 
                parsed_url.path.split('/')[1] == 'search')

    @staticmethod
    def remove_pagination_query_if_exists(results_page_url):
        # http://stackoverflow.com/questions/7734569/how-do-i-remove-a-query-string-from-url-using-python
        u = urlparse(results_page_url)
        query = parse_qs(u.query)
        if 's' not in query:
            return results_page_url

        query.pop('s')
        u = u._replace(query=urlencode(query, True))
        results_page_url = urlunparse(u)
        return results_page_url

    def extract_validated_data(self):
        email = self.validated_data['email']
        results_page_url = self.validated_data['results_page_url']
        return email, results_page_url

    def create_tracker(self):
        email, results_page_url = self.extract_validated_data()
        user, created = User.objects.get_or_create(email=email)
        user.save()
        data = get_current_listings(results_page_url)
        tracker = Tracker(user=user, results_page_url=results_page_url, listings=data)
        tracker.save()
        # send initial email with current listings
        send_confirmation_message(email, results_page_url, data)


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
