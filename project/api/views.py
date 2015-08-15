from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.exceptions import APIException

from dnsmanager.models import Zone

from ..account.filters import filter_zone_queryset
from ..account.models import Domain, Organisation
from .serializers import ZoneListSerializer
from .permissions import ReadOnlyPermissions, SuperUserOnlyPermissions


class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for DNS zones
    """
    serializer_class = ZoneListSerializer
    permission_classes = [ReadOnlyPermissions]  #[DjangoModelPermissions]
    lookup_field = 'domain__name'
    lookup_value_regex = '[^/]+'
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return filter_zone_queryset(Zone.objects.all(), self.request)


class ZoneFileUploadView(APIView):
    permission_classes = [SuperUserOnlyPermissions]  #[IsAuthenticated]
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