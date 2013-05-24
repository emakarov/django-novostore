# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.conf import settings
import logging
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.db.models import Q,F
from utils.visibility import VisibleManager, SuperUserVisibleManager, VisibleBaseUserManager, SuperUserVisibleBaseUserManager
#if settings.DEBUG:
#    logging.basicConfig(level = logging.DEBUG)

# Create your models here.

class AccountsUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    subscribed = models.BooleanField(_("Subscription"), default=False, help_text = _('Receive notifications by email?'))
    photo = models.CharField(_("Url To photo"), max_length=255, blank=True, default='', help_text = _("Url To photo"))
    birthday = models.DateField(_("Birthday"), null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    confirm_key = models.CharField(_("Confirmation Key"), max_length=30, blank=True, default='', help_text = _("Key for password restore"))
    photo_small_avatar = models.CharField(_("Url To small photo"), max_length=255, blank=True, default='/static/img/no_userpic.gif')
    is_worker = models.BooleanField(_("Is this user worker"), default=False, help_text = _("Whether this user worker or not?"))
    
    objects = SuperUserVisibleBaseUserManager(Q(id=lambda r:r.user.id) | 
                                     Q(worked__shop__owner=lambda r:r.user) 
                                    )