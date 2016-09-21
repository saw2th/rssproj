from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rssitem/(?P<item_id>[0-9]+)/$', views.item, name='item'),
    url(r'^search/$', views.search_items, name='search_items'),
    url(r'flag_item/(?P<item_id>[0-9]+)/$', views.flag_item, name='flag_item'),
]
