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
from photologue.models import ImageModel, Gallery, Photo
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import random
import string
from django.template.defaultfilters import slugify

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
  articles = blog_models.Article.objects.filter(terms__in = term, publish_status = '2')
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
  return render_to_response(article.template, params, context_instance = RequestContext(request))

def objects(request):
  termslug = 'objects'
  term = blog_models.Term.objects.filter(termslug = termslug)
  articles = blog_models.Article.objects.filter(terms__in = term, publish_status = '2')
  terms = blog_models.Term.objects.all().exclude(is_servicecat=True)
  params = { 'articles' : articles }
  return render_to_response('gsmrepiter/blog/objects.html', params, context_instance = RequestContext(request))

  
def redactorimagejson(request):
  photos = Photo.objects.all().order_by('-id')
  template = loader.get_template('redactorimagesjson.html')
  params = { 'photos' : photos }
  context = RequestContext(request, params)  
  return HttpResponse(template.render(context),mimetype='application/json')  

@csrf_exempt  
def uploadimagejson(request):
  p = Photo()
  print request.FILES.items()
  if request.user.is_authenticated():
    if request.method == 'POST':
      pt = codegenerator()+codegenerator()
      p.image = request.FILES['file']
      p.title = pt
      p.title_slug = slugify(pt) #+codegenerator()
      p.save()
#  template = loader.get_template('redactorimageupload.html')
    params = { 'photo' : p }
#  context = RequestContext(request, params)  
  return render_to_response('redactorimageupload.html',params,context_instance = RequestContext(request))
#  return HttpResponse(template.render(context),mimetype='application/json')  
        
    
def codegenerator():
  digits = "".join( [random.choice(string.digits) for i in xrange(3)] )
  chars = "".join( [random.choice(string.letters) for i in xrange(4)] ).lower()
  digits2 = "".join( [random.choice(string.digits) for i in xrange(3)] )
  return digits+chars+digits2