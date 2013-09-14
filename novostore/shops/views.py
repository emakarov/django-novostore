# Create your views here.
# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import Template,RequestContext, loader, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required
from photologue.models import Photo
from django.http import HttpResponse
# Create your views here.
from datetime import tzinfo, timedelta, datetime
from django.views.decorators.cache import never_cache
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import ugettext_noop
from django.utils.translation import get_language
from ncatalogue import models as ncatalogue_models
from django.db.models import Q,F
import models as shop_models

def sendmail(request):
    #email_to = 'olgavarenik@gmail.com'
    email_to = 'evgeni.makarov@gmail.com'
    ue = request.POST['name']
    text = request.POST['text']
    email = request.POST['email']
    subj = u'Отзыв с сайта Ольги Вареник' #request.POST['subj']
    message = text+u'\nИмя пользователя:'+ue+u'\nEmail пользователя:'+email
    mail.send_mail(subj, message, 'site@olgavarenik.ru', [ email_to ])
    mail.send_mail(subj, message, 'site@olgavarenik.ru', [ 'vj.workshop@gmail.com' ])
    mail.send_mail(subj, message, 'site@olgavarenik.ru', [ 'olgavarenik@gmail.com' ])
    #print message
    return render_to_response('email_send.html', [], context_instance = RequestContext(request))