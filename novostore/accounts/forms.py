from models import *
from django.contrib import auth
from django import forms

class AccountsUserFormShort(forms.ModelForm):

    class Meta:
        model = AccountsUser
        fields = ['first_name','last_name','subscribed']

class HRUserCreationForm(auth.forms.UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    #captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__exact = email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("User with this email already exists"))

    class Meta:
        model = AccountsUser
        fields = ('username', 'email')

class LoginForm(forms.Form):
    email_or_login = forms.CharField(max_length=100)
    password = forms.CharField()

    def clean_email_or_login(self):
        email_or_login = self.cleaned_data['email_or_login']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(email__exact = email_or_login, password = password)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("User with this credentials not found"))
