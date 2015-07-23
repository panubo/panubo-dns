from django.contrib import admin

from .models import Domain, Organisation, Membership


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'organisation', 'name',)
    list_filter = ('organisation', 'name')


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    list_filter = ('name',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'organisation')
    list_filter = ('user', 'organisation')