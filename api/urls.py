from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import UserTracker


urlpatterns = [
    url(r'^user-tracker/', UserTracker.as_view())
]
