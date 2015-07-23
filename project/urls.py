from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


from django.contrib import admin
admin.autodiscover()

admin.site.site_title = 'Panubo DNS'
admin.site.site_header = 'Panubo DNS'
admin.site.index_title = 'Administration'

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:login'), permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
)
