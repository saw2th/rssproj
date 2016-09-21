from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class RssItem(models.Model):
    """Holds an individual item in an rss feed"""
    title = models.TextField(blank=True, null=True, help_text="Title of rss item")
    summary = models.TextField(blank=True, null=True, help_text="Body of rss item")
    link = models.CharField(max_length=300, unique=True,blank=False, null=False, help_text="link to content")
    updated = models.DateTimeField(blank=True, null=True, help_text="date updated utc")

    def __unicode__(self):
        return self.title

    def item_flagged(self, user):
        """Is the item flagged for this user
        """
        return RssItemFlag.objects.filter(user=user, item=self).count() > 0


class RssItemFlag(models.Model):
    """Holds the record of an item that has been flagged by a user
    """
    user = models.ForeignKey(User)
    item = models.ForeignKey('RssItem')
