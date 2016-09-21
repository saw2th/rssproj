from django import template


register = template.Library()

@register.filter
def flagged(item, user):
    """return 'Flagged' if flagged else
    user must be logged in
    """
    return 'Flagged' if item.item_flagged(user) else 'Flag'
