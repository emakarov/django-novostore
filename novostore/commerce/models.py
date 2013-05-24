# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.extras.widgets import SelectDateWidget
#from honeyroiboos.blog.custom_widget import TinyMCE
from django.shortcuts import render_to_response
#from ncatalogue import models as ncat_models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.db.models import Sum
from django.core.validators import *
from django.db.models import Q,F
from utils.visibility import VisibleManager

class Currency(models.Model):
  name = models.CharField(_("Name"),max_length=50)
  shortname = models.CharField(_("Short name"),max_length=10)
  name_international = models.CharField(_("Name international"),max_length=50)
  shortname_international = models.CharField(_("Short name international"),max_length=10)
  #shop = models.ForeignKey(shop_models.Shop,verbose_name = _("Shop"),related_name='currencies')

  #objects = VisibleManager(Q(shop__owner=lambda r:r.user))

  
  def __unicode__(self):
    return "%s (%s)" % (self.name, self.shortname)
  
  class Meta:
    verbose_name = _("Currency")
    verbose_name_plural = _("Currencies")

from ncatalogue.models import Product


class Cart(models.Model):
    is_active = models.BooleanField(_("Is active"))
#    coupons_left = models.IntegerField()
#    coupons_purchased = models.IntegerField()
    #session_key = models.CharField(max_length=100,verbose_name=_("Session Store"),db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
    created_at = models.DateTimeField(_("Creation time"), auto_now_add = True)
    modified_at = models.DateTimeField(_("Last-modified time"), auto_now = True, auto_now_add = True)
    random_key = models.CharField(max_length=100,verbose_name=_("Random key for direct links"),db_index=True)

    #shop = models.ManyToManyField(shop_models.Shop,verbose_name = _("Shop"),related_name='carts')

    objects = VisibleManager(Q(elements__product__categories__shop__owner=lambda r:r.user))

    def __unicode__(self):
      return "%d %s"%(self.id, self.user)
        
    def number_of_items(self):
      return self.elements.all().aggregate(Sum('quantity'))

    class Meta:
      verbose_name = _("Cart")
      verbose_name_plural = _("Carts")

class CartElement(models.Model):
    product = models.ForeignKey(Product,verbose_name=_("Product"))
    quantity = models.IntegerField(_("Quantity"))
    cart = models.ForeignKey(Cart,verbose_name=_("Cart"),related_name="elements")

    objects = VisibleManager(Q(product__categories__shop__owner=lambda r:r.user))


    def sum(self):
      return self.product.price*self.quantity
    
    class Meta:
        verbose_name = _("Cart Element")
        verbose_name_plural = _("Cart Elements")

class PreOrder(models.Model):
#    cart = models.ForeignKey(Cart,verbose_name=_("Cart"))
#    coupons_number = models.IntegerField()
    paid = models.BooleanField()
#    price = models.FloatField()
    shopoholic = models.ForeignKey(settings.AUTH_USER_MODEL)
#    promocode = models.ForeignKey(PromoCode)
    created_at = models.DateTimeField(_("Creation time"), auto_now_add = True)
    modified_at = models.DateTimeField(_("Last-modified time"), auto_now = True, auto_now_add = True)
    requested_for_delivery = models.BooleanField(_("Waiting for delivery"), default = False)
    payment_on_delivery = models.BooleanField(_("Payment on delivery"), default = False)
    is_active = models.BooleanField(_("Is active"), default = True)

    objects = VisibleManager(Q(elements__product__categories__shop__owner=lambda r:r.user))
    
    def price(self):
      price = 0
      for el in self.elements.all():
        price += el.sum()
      return price

    price.verbose_name = _("Price")
    
    def __unicode__(self):
        return str(self.id)
        
    class Meta:
        verbose_name = _("Preorder")
        verbose_name_plural = _("Preorders")

class PreOrderElement(models.Model):
    product = models.ForeignKey(Product,verbose_name=_("Product"))
    quantity = models.IntegerField(_("Quantity"))
    preorder = models.ForeignKey(PreOrder,verbose_name=_("PreOrder"),related_name="elements")

    objects = VisibleManager(Q(product__categories__shop__owner=lambda r:r.user))


    def price(self):
      return self.product.price

    def sum(self):
      return self.product.price*self.quantity
    
    price.verbose_name = _("Price")
    sum.verbose_name = _("Sum")


    class Meta:
        verbose_name = _("Cart Element")
        verbose_name_plural = _("Cart Elements")


    
class CurrencyExchange(models.Model):
    from_currency = models.ForeignKey(Currency,related_name="from_exchange_rates",verbose_name=_("From currency"))
    to_currency = models.ForeignKey(Currency,related_name="to_exchange_rates",verbose_name=_("To currency"))
    course = models.FloatField(_("Course"))
    
    class Meta:
        verbose_name = _("Currency Exchange")
        verbose_name_plural = _("Currency Exchange")

class Tariff(models.Model):
    name = models.CharField(_("Name"),max_length = 255)
    price = models.FloatField(_("Price"))
    quantity = models.IntegerField(_("Quantity of items"),default=1)
    currency = models.ForeignKey(Currency,verbose_name=_("Currency"))
    product = models.ForeignKey(Product,verbose_name=_("Product"),related_name="tarrifs")

    def __unicode__(self):
        return unicode(self.name)
        
    class Meta:
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")


class PromoPartner(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name of partner"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True, verbose_name=_('User for this promo partner account'))
    
    def __unicode__(self):
        return u'%s' % self.name 
    
    class Meta:
        verbose_name = _("Promo Partner")
        verbose_name_plural = _("Promo Partners")


class PromoCode(models.Model):
    promoparnter = models.ForeignKey(PromoPartner,parent_link=True,verbose_name=_('Promo Partner'))
    code = models.CharField(_("Code"), max_length = 255, blank = True, default = '', help_text = "Promo Code")
    discount = models.FloatField(_("Discount in percentage"))
    number_of_activations_allowed = models.IntegerField(_("Number Of Activations Allowed"), default=1)
    number_of_activations_made = models.IntegerField(_("Number Of Activations Made"), default=0) 

    def __unicode__(self):
        return u'%s' % self.code 

    class Meta:
        verbose_name = _("Promo Code")
        verbose_name_plural = _("Promo Codes")

class DeliveryAddress(models.Model):
    city = models.CharField(max_length=255, verbose_name=_("City"), null=True, blank = True)
    street_house = models.CharField(max_length=255, verbose_name=_("Street and house"), null=True, blank = True)
    zipcode = models.CharField(_("Zip Code"), max_length = 255, null=True, blank = True, help_text = "Zip Code")
    lat = models.FloatField(verbose_name=_("Latitude"),help_text=_('Location'),
            validators=[MinValueValidator(-90),MaxValueValidator(90)],blank=True,null=True)
    lon = models.FloatField(verbose_name=_("Longitutde"),help_text=_('Location'),
            validators=[MinValueValidator(-180),MaxValueValidator(180)],blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("User"),related_name = 'delivery_addresses')
    phone = models.CharField(_("Phone"), max_length = 255, null=True, blank = True, help_text = "Phone")
            
    def __unicode__(self):
        return u'%s %s' % (self.city,self.street_house)

    class Meta:
        verbose_name = _("Delivery Address")
        verbose_name_plural = _("Delivery Addresses")

