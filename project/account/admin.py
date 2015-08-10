from django.contrib import admin

from .models import Domain, Organisation, Membership


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0
    can_delete = False


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'organisation', 'name',)
    list_filter = ('organisation',)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    list_filter = ('name',)
    inlines = (MembershipInline, DomainInline)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'organisation')
    list_filter = ('user', 'organisation')