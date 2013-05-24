from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.util import quote, get_fields_from_path
from django.contrib.admin.filterspecs import FilterSpec,RelatedFilterSpec
from django.contrib.admin.util import get_model_from_relation
from django.db import models
from django.utils.encoding import smart_unicode

class FilterControlChangeList(ChangeList):
    """
    This ancestor of the ChangeList allows to control created FilterSpec
    using additional admin method get_filter_spec(self,field, request, params,
    model, model_admin, field_path=None) introduced in a FilterControlMixin class.

    Object of this class is created by FilterControlMixin class present below.
    """
    def get_filters(self, request):
        filter_specs = []
        if self.list_filter:
            for filter_name in self.list_filter:
                field = get_fields_from_path(self.model, filter_name)[-1]

                spec = self.model_admin.get_filter_spec(field, request, self.params,
                                         self.model, self.model_admin,
                                         field_path=filter_name)
                if not spec:
                    spec = FilterSpec.create(field, request, self.params,
                                         self.model, self.model_admin,
                                         field_path=filter_name)
                if spec and spec.has_output():
                    filter_specs.append(spec)
        return filter_specs, bool(filter_specs)

class FilteredRelatedFilterSpec(RelatedFilterSpec):
    """
    This ancestor of the RelatedFilterSpec uses get_lookup_queryset
    to get queryset (or other iterable) of objects to be used as a filter.
    """
    def __init__(self, f, request, params, model, model_admin,
                 field_path=None):
        #BAD HACK!!!
        super(RelatedFilterSpec, self).__init__(
            f, request, params, model, model_admin, field_path=field_path)

        # others stored in parent
        self.request = request
        self.model = model
        self.model_admin = model_admin
        
        other_model = get_model_from_relation(f)
        if isinstance(f, (models.ManyToManyField,
                          models.related.RelatedObject)):
            # no direct field on this model, get name from other model
            self.lookup_title = other_model._meta.verbose_name
        else:
            self.lookup_title = f.verbose_name # use field name
        rel_name = other_model._meta.pk.name

        self.lookup_kwarg = '%s__%s__exact' % (self.field_path, rel_name)
        self.lookup_kwarg_isnull = '%s__isnull' % (self.field_path)
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_val_isnull = request.GET.get(
                                      self.lookup_kwarg_isnull, None)
        self.lookup_choices = self.get_lookup_choices()

    def get_lookup_choices(self):
        """
        Returns list of tuple(pk_value,name) to be used as a filter choices.
        """
        queryset = self.get_lookup_queryset()
        lst = [(x._get_pk_val(), smart_unicode(x)) for x in queryset]
        return lst

    def get_lookup_queryset(self):
        """
        Returns queryset or other iterable, containing objects to be used as a filter choices.

        Overwrite this method to return your own queryset or list of objects to be present
        as a filter.
        """
        return self.field.rel.to._default_manager.all()

class AdminFilteredRelatedFilterSpec(FilteredRelatedFilterSpec):
    """
    This ancestor of the FilteredRelatedFilterSpec uses model admin
    instance to get queryset of objects to be used as a filter.

    You can create instance of this class in FilterControlMixin.get_filter_spec
    instance method instead of declaring a new ancestor of the FilteredRelatedFilterSpec class.

    Pass related objects admin instance to related_admin_instance additional parameter
    of the constructor. You can use syntax like YourModelAdmin(YourModel,self.admin_site) to construct
    a new instance of the related model admin.
    """
    def __init__(self, f, request, params, model, model_admin, related_admin_instance=None, field_path=None):
        self.related_admin_instance = related_admin_instance
        super(AdminFilteredRelatedFilterSpec,self).__init__(f, request, params, model, model_admin, field_path=field_path)
    def get_lookup_queryset(self):
        if self.related_admin_instance:
            return self.related_admin_instance.queryset(self.request)
        return []

class VisibleFilteredRelatedFilterSpec(FilteredRelatedFilterSpec):
    """
    This ancestor of the FilteredRelatedFilterSpec uses model visibility manager
    instance to get queryset of objects to be used as a filter.

    You can create instance of this class in FilterControlMixin.get_filter_spec
    instance method instead of declaring a new ancestor of the FilteredRelatedFilterSpec class.
    """
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(VisibleFilteredRelatedFilterSpec,self).__init__(f, request, params, model, model_admin, field_path=field_path)
    def get_lookup_queryset(self):
        if hasattr(self.field.rel.to._default_manager,'visible'):
            return self.field.rel.to._default_manager.visible(self.request)
        return []

class FilterControlMixin(object):
    """
    This mixin for ModelAdmin or it's ancestor overrides ModelAdmin ChangeList filter behaviour.

    In order to work it should precede ModelAdmin in base class list for user's admin class.

    As a result, you can create your own django.contrib.admin.filterspecs.FilterSpec ancestor
    for specific field, instead of standard one. Use f.e. FilteredRelatedFilterSpec or
    AdminFilteredRelatedFilterSpec for the purpose.

    You should override get_filter_spec method and return instance of your own filter. If
    you don't, the standard filter will be used as a fall back.
    """
    def get_changelist(self, request, **kwargs):
        return FilterControlChangeList

    def get_filter_spec(self,field, request, params, model, model_admin, field_path=None):
        return None
