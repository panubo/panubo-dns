from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.exceptions import APIException

from ..account.filters import filter_zone_queryset, filter_zonerecord_queryset
from ..account.models import Domain, Organisation
from .serializers import *
from .permissions import ReadOnlyPermissions, SuperUserOnlyPermissions


class ZoneViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyPermissions, SuperUserOnlyPermissions]
    lookup_field = 'domain__name'
    lookup_value_regex = '[^/]+'
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return filter_zone_queryset(Zone.objects.all(), self.request)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ZoneListSerializer
        return super(ZoneViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ZoneDetailSerializer
        return super(ZoneViewSet, self).retrieve(request, *args, **kwargs)


class AddressRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = AddressRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(AddressRecord.objects.all(), self.request)


class CanonicalNameRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = CanonicalNameRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(CanonicalNameRecord.objects.all(), self.request)


class MailExchangeRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = MailExchangeRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(MailExchangeRecord.objects.all(), self.request)


class NameServerRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = NameServerRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(NameServerRecord.objects.all(), self.request)


class TextRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = TextRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(TextRecord.objects.all(), self.request)


class ServiceRecordViewSet(viewsets.ModelViewSet):

    permission_classes = [SuperUserOnlyPermissions]
    serializer_class = ServiceRecordSerializer

    def get_queryset(self):
        return filter_zonerecord_queryset(ServiceRecord.objects.all(), self.request)


class ZoneFileUploadView(APIView):
    permission_classes = [SuperUserOnlyPermissions]
    parser_classes = (parsers.FileUploadParser,)

    def _get_or_create_zone(self, domain, user):
        try:
            return Zone.objects.get(domain__name=domain)
        except Zone.DoesNotExist:
            # if user in one organisation
            if user.organisations.count() == 1:
                org = Organisation.objects.get(members__user=user)
                domain_obj, created = Domain.objects.get_or_create(organisation=org, name=domain)
                return Zone.objects.create(domain=domain_obj)
            else:
                raise APIException(detail="Cannot create Zone. User exists in many organisations and there is no default")

    def post(self, request, domain, format=None):
        if request.FILES.get('data'):
            data = request.FILES.get('data').read()
        else:
            data = request.data.get('data', None)

        if data is not None:
            zone = self._get_or_create_zone(domain, request.user)
            success, msg = zone.update_from_text(data)
        else:
            msg = 'No data payload received'
            success = False

        if success:
            return Response(status=status.HTTP_201_CREATED, data=msg, content_type='text/plain')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=msg, content_type='text/plain')