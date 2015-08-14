from django.contrib import admin

from .models import Domain, Organisation, Membership

from dnsmanager.models import Zone
from dnsmanager.admin import ZoneAdmin as ZoneAdminSuper


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0
    can_delete = False


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class OrganisationListFilter(admin.SimpleListFilter):
    """ Limit the List filter to valid options for the user """
    title = 'Organisation'
    parameter_name = 'organisation__id__exact'

    def lookups(self, request, model_admin):
        # TODO: Add different filtering for super users
        my_orgs = set([m.organisation for m in Membership.objects.filter(user=request.user)])
        return [(m.pk, m.name) for m in my_orgs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(organisation_id=self.value())
        else:
            return queryset


class DomainOrganisationListFilter(OrganisationListFilter):
    """ Limit the List filter to valid options for the user """
    parameter_name = 'domain_organisation__id__exact'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(domain__organisation_id=self.value())
        else:
            return queryset


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'organisation', 'name',)
    list_filter = (OrganisationListFilter,)

    def get_queryset(self, request):
        """ Limit results to qs """
        qs = super(DomainAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organisation__pk__in=request.user.organisations.values_list('organisation_id', flat=True))

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """ Limit choices for 'organisation' field """
        if db_field.name == 'organisation':
            if not request.user.is_superuser:
                kwargs["queryset"] = Organisation.objects.filter(
                    pk__in=request.user.organisations.values_list('organisation_id', flat=True))
        return super(DomainAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    list_filter = ('name',)
    inlines = (MembershipInline, DomainInline)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'organisation')
    list_filter = ('user', 'organisation')


admin.site.unregister(Zone)

@admin.register(Zone)
class ZoneAdmin(ZoneAdminSuper):
    list_filter = (DomainOrganisationListFilter,)

    def get_queryset(self, request):
        """ Limit results to qs """
        qs = super(ZoneAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(domain__organisation_id__in=request.user.organisations.values_list('organisation_id', flat=True))

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """ Limit choices for 'domain' field """
        if db_field.name == 'domain':
            if not request.user.is_superuser:
                kwargs["queryset"] = Domain.objects.filter(organisation_id__in=request.user.organisations.values_list('organisation_id', flat=True))
        return super(ZoneAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
