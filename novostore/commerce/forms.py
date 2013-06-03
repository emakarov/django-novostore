from django import forms
from django.conf import settings
from commerce import models as commerce_models

class DeliveryAddressForm(forms.ModelForm):
  class Meta:
    model = commerce_models.DeliveryAddress
    exclude = ('lat','lon','user')
    
class DeliveryAddressFormWithUser(forms.ModelForm):
  class Meta:
    model = commerce_models.DeliveryAddress
    exclude = ('lat','lon')