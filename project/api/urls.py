from django.conf.urls import patterns, include, url

from rest_framework import routers
import views

router = routers.DefaultRouter()

#router.register(r'domains', views.DomainViewSet)
router.register(r'zones', views.ZoneViewSet, base_name='zones')

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    #url(r'^v1/zonelist/', views.ZoneListView.as_view(), name='zone-list'),
    url(r'^v1/zone-upload/(?P<domain>.+)/$', views.ZoneFileUploadView.as_view(), name='zone-upload'),
    url(r'^v1/zone-upload/(?P<domain>.+)/\.(?P<format>[a-z0-9]+)$', views.ZoneFileUploadView.as_view(), name='zone-upload'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)