from rest_framework import serializers
from rest_framework.exceptions import ParseError
from dnsmanager.models import AddressRecord, CanonicalNameRecord, MailExchangeRecord, NameServerRecord, TextRecord, \
    ServiceRecord, Zone

from ..account.models import Domain


class AddressRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'ip', 'ttl')
        model = AddressRecord


class CanonicalNameRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'target', 'ttl')
        model = CanonicalNameRecord


class MailExchangeRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'priority', 'origin', 'ttl')
        model = MailExchangeRecord


class NameServerRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'origin', 'ttl')
        model = NameServerRecord


class TextRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'text', 'ttl')
        model = TextRecord


class ServiceRecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','data', 'priority', 'weight', 'port', 'target', 'ttl')
        model = ServiceRecord


class ZoneListSerializer(serializers.ModelSerializer):

    organisation = serializers.CharField(source='domain.organisation', read_only=True)
    domain = serializers.CharField(source='domain.name', read_only=True)
    is_valid = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = Zone
        fields = ('organisation', 'domain', 'is_valid', 'updated')

    def restore_object(self, attrs, instance=None):
        # Set domain id from domain name
        try:
            domain_id = Domain.objects.get(name=self.init_data.get('domain')).pk
        except Domain.DoesNotExist:
            raise ParseError('Domain matching query does not exist')
        attrs.update({'domain_id': domain_id})
        return super(self.__class__, self).restore_object(attrs, instance=instance)


class ZoneDetailSerializer(serializers.ModelSerializer):

    organisation = serializers.CharField(source='domain.organisation', read_only=True)
    domain = serializers.CharField(source='domain.name', read_only=True)
    data = serializers.CharField(source='render', read_only=True)
    is_valid = serializers.BooleanField(read_only=True, required=False)

    addressrecords = AddressRecordSerializer(many=True) #r(queryset, context={'request': request})
    canonicalnamerecords = CanonicalNameRecordSerializer(many=True)
    mailexchangerecords = MailExchangeRecordSerializer(many=True)
    nameserverrecords = NameServerRecordSerializer(many=True)
    textrecords = TextRecordSerializer(many=True)
    servicerecords = ServiceRecordSerializer(many=True)

    class Meta:
        model = Zone
        fields = ('organisation', 'domain', 'is_valid', 'data', 'updated',
                  'addressrecords',
                  'canonicalnamerecords',
                  'mailexchangerecords',
                  'nameserverrecords',
                  'textrecords',
                  'servicerecords')

    def restore_object(self, attrs, instance=None):
        # Set domain id from domain name
        try:
            domain_id = Domain.objects.get(name=self.init_data.get('domain')).pk
        except Domain.DoesNotExist:
            raise ParseError('Domain matching query does not exist')
        attrs.update({'domain_id': domain_id})
        return super(self.__class__, self).restore_object(attrs, instance=instance)