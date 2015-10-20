from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


from django.contrib import admin
admin.autodiscover()

admin.site.site_title = 'Panubo DNS'
admin.site.site_header = 'Panubo DNS'
admin.site.index_title = 'Administration'

extra_context = {'site_title': 'Panubo DNS', 'site_header': 'Panubo DNS',}

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:login'), permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', {'extra_context': extra_context}, name='admin_password_reset'),
    url(r'^accounts/', include('django.contrib.auth.urls'), {'extra_context': extra_context}),
    url(r'^api/', include('project.api.urls')),
    url(r'^zone/', include('dnsmanager.urls')),
)