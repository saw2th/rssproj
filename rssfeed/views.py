from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rssfeed.models import RssItem
from rssfeed.models import RssItemFlag


def index(request):
    """show a list rss items
    """
    rss_items = RssItem.objects.order_by('-updated')[:10]
    output = ', '.join([ri.title for ri in rss_items])
    return HttpResponse(output)

def item(request, item_id):
    """show an rss item
    """
    rss_item = get_object_or_404(RssItem, pk=item_id)
    output = ', '.join([rss_item.title, rss_item.summary])
    return HttpResponse(output)

def search_items(request):
    # get post request for search
    output = ''
    query = request.POST.get('q')
    if query:
        rss_items = RssItem.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )
        output += ', '.join([ri.title for ri in rss_items])

    return HttpResponse(output)

def flag_item(request, item_id):
    if request.user.is_authenticated() and request.method == 'POST':
        try:
            rss_item = RssItem.objects.get(pk=item_id)
        except RssItem.DoesNotExist:
            return HttpResponse('no object')

        RssItemFlag.objects.create(
            user=request.user,
            item=rss_item
        )

        return HttpResponse('flagged')
    return HttpResponse('you must be logged in')
