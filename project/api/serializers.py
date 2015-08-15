from rest_framework import serializers
from rest_framework.exceptions import ParseError
from dnsmanager.models import Zone

from ..account.models import Domain


class ZoneListSerializer(serializers.ModelSerializer):

    organisation = serializers.CharField(source='domain.organisation', read_only=True)
    domain = serializers.CharField(source='domain.name', read_only=True)
    data = serializers.CharField(source='render', read_only=True)
    is_valid = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = Zone
        fields = ('organisation', 'domain', 'is_valid', 'data', 'updated')

    def restore_object(self, attrs, instance=None):
        # Set domain id from domain name
        try:
            domain_id = Domain.objects.get(name=self.init_data.get('domain')).pk
        except Domain.DoesNotExist:
            raise ParseError('Domain matching query does not exist')
        attrs.update({'domain_id': domain_id})
        return super(self.__class__, self).restore_object(attrs, instance=instance)