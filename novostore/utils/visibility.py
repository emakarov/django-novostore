from django.contrib.admin.views.main import ChangeList
import operator
from functools import reduce

from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.core.paginator import InvalidPage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_str, force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.utils.http import urlencode

from django.contrib.admin import FieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.util import (quote, get_fields_from_path,
    lookup_needs_distinct, prepare_lookup_value)
from django.contrib import admin
from django.utils.copycompat import deepcopy
from django.db.models import Q, F
from mptt.managers import TreeManager
#from base_restricted_admin import *
 
from django.contrib.auth.models import BaseUserManager, UserManager
from django.core.exceptions import PermissionDenied, ValidationError

from django.contrib.auth.admin import UserAdmin

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField



    
class VisibleChangeList(ChangeList):
    def get_query_set(self, request):
        # First, we collect all the declared list filters.
        (self.filter_specs, self.has_filters, remaining_lookup_params,
         use_distinct) = self.get_filters(request)

        # Then, we let every list filter modify the queryset to its liking.
        qs = self.root_query_set
        for filter_spec in self.filter_specs:
            new_qs = filter_spec.queryset(request, qs)
            if new_qs is not None:
                qs = new_qs

        try:
            # Finally, we apply the remaining lookup parameters from the query
            # string (i.e. those that haven't already been processed by the
            # filters).
            qs = qs.filter(**remaining_lookup_params)
        except (SuspiciousOperation, ImproperlyConfigured):
            # Allow certain types of errors to be re-raised as-is so that the
            # caller can treat them in a special way.
            raise
        except Exception as e:
            # Every other error is caught with a naked except, because we don't
            # have any other way of validating lookup parameters. They might be
            # invalid if the keyword arguments are incorrect, or if the values
            # are not in the correct type, so we might get FieldError,
            # ValueError, ValidationError, or ?.
            raise IncorrectLookupParameters(e)

        # Use select_related() if one of the list_display options is a field
        # with a relationship and the provided queryset doesn't already have
        # select_related defined.
        if not qs.query.select_related:
            if self.list_select_related:
                qs = qs.select_related()
            else:
                for field_name in self.list_display:
                    try:
                        field = self.lookup_opts.get_field(field_name)
                    except models.FieldDoesNotExist:
                        pass
                    else:
                        if isinstance(field.rel, models.ManyToOneRel):
                            qs = qs.select_related()
                            break

        # Set ordering.
        ordering = self.get_ordering(request, qs)
        qs = qs.order_by(*ordering)

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        if self.search_fields and self.query:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in self.search_fields]
            for bit in self.query.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                qs = qs.filter(reduce(operator.or_, or_queries))
            if not use_distinct:
                for search_spec in orm_lookups:
                    if lookup_needs_distinct(self.lookup_opts, search_spec):
                        use_distinct = True
                        break

        if use_distinct:
            return self.model.objects.visible(request).distinct()
        else:
            return self.model.objects.visible(request)

class VisibleManager(models.Manager):

#   def __init__(self,q):
#     models.Manager.__init__(self)
#     self.q = q
#   
#   def visible(self,qs,request):
#       return qs.filter(self.q(request))

    def __init__(self,*args,**kw):
        super(VisibleManager,self).__init__()
        q  = None
        if len(args):
            q = args[0]
        if not q:
            q = Q(**kw)
        self.Q = q

    def set_values(self,q,request):
        for i in range(len(q.children)):
            if isinstance(q.children[i],Q):
                self.set_values(q.children[i],request)
                continue
            if callable(q.children[i]):
                callback = q.children[i]
                q.children[i] = callback(request)
                continue
            if not hasattr(q.children[i],'__getitem__'):
                continue
            if callable(q.children[i][1]):
                callback = q.children[i][1]
                q.children[i] = (q.children[i][0],callback(request))

    def visible(self,request):
        #if request.user.is_superuser:
        #    return self.get_query_set()
        q = deepcopy(self.Q)
        self.set_values(q,request)
        queryset = self.get_query_set().filter(q).distinct()
        return queryset
        
class SuperUserVisibleManager(VisibleManager):
    def visible(self,request):
        if request.user.is_superuser:
            return self.get_query_set()
        q = deepcopy(self.Q)
        self.set_values(q,request)
        queryset = self.get_query_set().filter(q).distinct()
        return queryset

class VisibleAdminMethods(object):

    def queryset_visible(self,request):
        if hasattr(self.model.objects,'visible'):
            return self.model.objects.visible(request)
        return self.model.objects.all()

    def formfield_queryset_visible(self, field, request, **kwargs):
        if hasattr(field,'rel') and hasattr(field.rel,'to') and hasattr(field.rel.to._default_manager,'visible'):
            return field.rel.to._default_manager.visible(request)

       
class VisibleAdmin(admin.ModelAdmin,VisibleAdminMethods):
    def queryset(self,request):
        return self.queryset_visible(request)

    def get_changelist(self, request, **kwargs):
      return VisibleChangeList

    def get_object(self, request, object_id):
        """
        Returns an instance matching the primary key provided. ``None``  is
        returned if no match is found (or the object_id failed validation
        against the primary key field).
        """
        queryset = self.queryset(request)
        model = queryset.model

        try:
            object_id = model._meta.pk.to_python(object_id)
            return queryset.get(pk=object_id)
        except (model.DoesNotExist, ValidationError):
            return None



    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a database Field that has declared choices.
        """
        # If the field is named as a radio_field, use a RadioSelect
        if db_field.name in self.radio_fields:
            # Avoid stomping on custom widget/choices arguments.
            if 'widget' not in kwargs:
                kwargs['widget'] = widgets.AdminRadioSelect(attrs={
                    'class': get_ul_class(self.radio_fields[db_field.name]),
                })
            if 'choices' not in kwargs:
                kwargs['choices'] = db_field.get_choices(
                    include_blank=db_field.blank,
                    blank_choice=[('', _('None'))]
                )
        return db_field.formfield(**kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        qs = self.formfield_queryset_visible(db_field, request, **kwargs)
        if qs != None:
            kwargs["queryset"] = qs
        return super(VisibleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        qs = self.formfield_queryset_visible(db_field, request, **kwargs)
        if qs != None:
            kwargs["queryset"] = qs
        return super(VisibleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        
        
class VisibilityTabularInline(admin.TabularInline, VisibleAdminMethods):
    def queryset(self,request):
        return self.queryset_visible(request)

    def get_changelist(self, request, **kwargs):
      return VisibleChangeList

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        qs = self.formfield_queryset_visible(db_field, request, **kwargs)
        if qs != None:
            kwargs["queryset"] = qs
        return super(VisibilityTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        qs = self.formfield_queryset_visible(db_field, request, **kwargs)
        if qs != None:
            kwargs["queryset"] = qs
        return super(VisibilityTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class VisibleTreeManager(TreeManager,VisibleManager):
  pass

class VisibleBaseUserManager(BaseUserManager,VisibleManager):
  pass

class SuperUserVisibleBaseUserManager(BaseUserManager,SuperUserVisibleManager):
    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        print "HERE DETECTION"
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=BaseUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    pass
      

class AccountsUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        from accounts.models import AccountsUser
        model = AccountsUser
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AccountsUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountsUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        from accounts.models import AccountsUser
        model = AccountsUser
        #fields = ['username', 'email', 'password', 'is_active', 'is_superuser']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountsUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = AccountsUserChangeForm
    add_form = AccountsUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email', 'is_superuser')
    list_filter = ('is_superuser',)
#    fieldsets = (
#        (None, {'fields': ('email', 'password')}),
#        ('Permissions', {'fields': ('is_admin',)}),
#        ('Important dates', {'fields': ('last_login',)}),
#    )
#    add_fieldsets = (
#        (None, {
#            'classes': ('wide',),
#            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
#        ),
#    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class VisibleUserAdmin(AccountsUserAdmin, VisibleAdminMethods):
    def queryset(self,request):
        return self.queryset_visible(request)