from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

class User(models.Model):
    email = models.EmailField(primary_key=True)


class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    results_page_url = models.URLField(max_length=500)
    listings = JSONField()
