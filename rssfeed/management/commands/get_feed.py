from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError, transaction

import feedparser

from rssfeed.models import RssItem


class Command(BaseCommand):
    help = "load the contents of an rss feed"

    def handle(self, *args, **options):
         "load rss feed"
         rss_feed = feedparser.parse(settings.DEFAULT_RSS_FEED)
         for item in rss_feed.get('entries', []):
             try:
                 with transaction.atomic():
                     RssItem.objects.create(
                         title=item.get('title'),
                         link=item.get('link'),
                         summary=item.get('summary'),
                         updated=item.get('updated')
                     )
             except IntegrityError:
                 print "rssitem already present"
                 
