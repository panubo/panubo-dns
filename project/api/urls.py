from django.conf.urls import patterns, include, url

from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'zones', views.ZoneViewSet, base_name='zones')
router.register(r'addressrecords', views.AddressRecordViewSet, base_name='addressrecords')
router.register(r'canonicalnamerecords', views.CanonicalNameRecordViewSet, base_name='canonicalnamerecords')
router.register(r'mailexchangerecords', views.MailExchangeRecordViewSet, base_name='mailexchangerecords')
router.register(r'nameserverrecords', views.NameServerRecordViewSet, base_name='nameserverrecords')
router.register(r'textrecords', views.TextRecordViewSet, base_name='textrecords')
router.register(r'servicerecords', views.ServiceRecordViewSet, base_name='servicerecords')

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    url(r'^v1/zone-upload/(?P<domain>.+)/$', views.ZoneFileUploadView.as_view(), name='zone-upload'),
    url(r'^v1/zone-upload/(?P<domain>.+)/\.(?P<format>[a-z0-9]+)$', views.ZoneFileUploadView.as_view(), name='zone-upload'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)