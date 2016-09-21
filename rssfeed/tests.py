from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User

from unipath import Path

from rssfeed.models import RssItem
from rssfeed.models import RssItemFlag


class RssFeedParserTest(TestCase):
    """Test rssfeed management command
    Should populate RssItem model
    """

    def test_read_feed(self):
        # override default rss setting
        with self.settings(
                DEFAULT_RSS_FEED=unicode(
                    Path('.', 'rssfeed', 'test_data', 'slashdotMain').absolute()
                )
        ):
            call_command('get_feed')
            rss_items = RssItem.objects.all()
            self.failUnlessEqual(
                rss_items.count(),
                15
            )

            # call get_feed again - unique constraint on link
            # will ensure only one of each RssItems is saved
            call_command('get_feed')
            rss_items = RssItem.objects.all()
            self.failUnlessEqual(
                rss_items.count(),
                15
            )

class RssItemDisplayTest(TestCase):
    """Test the display of the rss items
    """

    fixtures = [
        'rssitems.json',
        'users.json'
    ]

    def test_show_rss_item_list(self):
        response = self.client.get('/')
        self.assertContains(
            response,
            'An rss item title',
            status_code=200
        )
        self.assertNotContains(
            response,
            'button',
            status_code=200
        )


    def test_show_rss_item_list_user_logged_in(self):
        logged_in = self.client.login(
            username='stephen',
            password='lastword'
        )
        response = self.client.get('/')
        self.assertContains(
            response,
            'button',
            status_code=200
        )

    def test_show_rss_item_item(self):
        response = self.client.get('/rssitem/2/')
        self.assertContains(
            response,
            'Another rss item',
            status_code=200
        )

    def test_search_rss_items(self):
        response = self.client.post('/search/', {'q': 'another'})
        self.assertContains(
            response,
            'Another rss item',
            status_code=200
        )

        response = self.client.post('/search/', {'q': 'summary'})
        self.assertContains(
            response,
            'An rss item title',
            status_code=200
        )

    def test_flag_item(self):
        rss_item_flags = RssItemFlag.objects.all()

        self.failUnlessEqual(
            rss_item_flags.count(),
            0
        )
        logged_in = self.client.login(
            username='stephen',
            password='lastword'
        )
        response = self.client.post('/flag_item/1/', {})
        rss_item_flags = RssItemFlag.objects.all()
        self.failUnlessEqual(
            rss_item_flags.count(),
            1
        )
        self.failUnlessEqual(
            RssItem.objects.get(id=1).item_flagged(
                User.objects.get(username='stephen')
            ),
            True
        )

    def test_flag_item_get_request(self):
        logged_in = self.client.login(
            username='stephen',
            password='lastword'
        )
        response = self.client.get('/flag_item/1/')
        rss_item_flags = RssItemFlag.objects.all()
        self.failUnlessEqual(
            rss_item_flags.count(),
            0
        )

    def test_flag_item_not_logged_in(self):
        response = self.client.post('/flag_item/1/', {})

        rss_item_flags = RssItemFlag.objects.all()
        self.failUnlessEqual(
            rss_item_flags.count(),
            0
        )
