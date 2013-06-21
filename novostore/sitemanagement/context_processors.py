from models import WebsiteMenu
from django.db.models import Q,F

def menu_context(context):
    topmenu = None
    try:
      topmenu = WebsiteMenu.objects.filter(Q(parent__id=2) | Q(parent__parent__id=2))
    except:
      pass
    return { 'topmenu' : topmenu }    
