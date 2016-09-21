from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render

from rssfeed.models import RssItem
from rssfeed.models import RssItemFlag


def index(request):
    """show a list rss items
    """
    rss_items = RssItem.objects.order_by('-updated')[:10]
    context = {
        'rss_items': rss_items,
        'user_logged_in': request.user.is_authenticated()
    }
    return render(request, 'rssfeed/index.html', context)

def item(request, item_id):
    """show an rss item
    """
    rss_item = get_object_or_404(RssItem, pk=item_id)
    context = {'item': rss_item}
    return render(request, 'rssfeed/item.html', context)

def search_items(request):
    # get post request for search
    context = {'search': True}
    query = request.POST.get('q')
    if query:
        rss_items = RssItem.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )
        context.update({
            'rss_items': rss_items,
            'rss_items_count': rss_items.count(),
            'user_logged_in': request.user.is_authenticated(),
            'query':  query
        })

    return render(request, 'rssfeed/index.html', context)

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
