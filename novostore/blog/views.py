# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import Template,RequestContext, loader, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
from datetime import tzinfo, timedelta, datetime
from django.views.decorators.cache import never_cache
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import ugettext_noop
from django.utils.translation import get_language
from blog import models as blog_models
from django.db.models import Q,F

blog_index_html = settings.BLOG_INDEX_HTML
blog_articlelist_html = settings.BLOG_ARTICLELIST_HTML
blog_article_html = settings.BLOG_ARTICLE_HTML

def index(request):
  articles = blog_models.Article.objects.filter(publish_status = '2')
  terms = blog_models.Term.objects.all().exclude(is_servicecat=True)
  params = { 'articles' : articles, 'terms' : terms }
  return render_to_response(blog_index_html(request), params, context_instance = RequestContext(request))
  
def blogtermpage(request,termslug):
  term = blog_models.Term.objects.filter(termslug = termslug)
  articles = blog_models.Article.objects.filter(terms__in = term, publish_status = '2').exclude(cover=None)
  terms = blog_models.Term.objects.all().exclude(is_servicecat=True)
  params = { 'articles' : articles, 'terms' : terms }
  return render_to_response(blog_articlelist_html(request), params, context_instance = RequestContext(request))

def search(request):
    q = None
    try:
      q = request.GET['s']
    except:
      pass
    if q:
      articles = blog_models.Article.objects.filter(Q(title__icontains=q) | Q(text__icontains=q), publish_status = '2')
    else:
      articles = blog_models.Article.all().none()
    terms = blog_models.Term.objects.all().exclude(is_servicecat=True)
    params = { 'articles' : articles, 'terms' : terms }
    return render_to_response(blog_articlelist_html(request), params, context_instance = RequestContext(request))
  
def article(request,artid):
  article = blog_models.Article.objects.get(id=artid)
  sidebar = blog_models.Article.objects.filter(publish_status = '2').exclude(id=artid).order_by('?')[0:20]
  terms = blog_models.Term.objects.all().exclude(is_servicecat=True)
  params = { 'article' : article, 'sidebar' : sidebar, 'terms' : terms }
  return render_to_response(blog_article_html(request), params, context_instance = RequestContext(request))