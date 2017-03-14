from rest_framework import serializers
from rest_framework.exceptions import ParseError
from dnsmanager.models import AddressRecord, CanonicalNameRecord, MailExchangeRecord, NameServerRecord, TextRecord, \
    ServiceRecord, Zone

from ..account.models import Domain


class AddressRecordSerializer(serializers.ModelSerializer):

    domain = serializers.CharField(source='zone.domain')

    class Meta:
        fields = ('id','data', 'ip', 'ttl', 'domain')
        model = AddressRecord

    def create(self, validated_data):
        zone = Zone.objects.get(domain__name=validated_data['zone']['domain'])
        obj = AddressRecord(zone=zone,
                                  data=validated_data['data'],
                                  ip=validated_data['ip'],
                                  ttl=validated_data['ttl'])
        obj.save()
        return obj


class CanonicalNameRecordSerializer(serializers.ModelSerializer):

    domain = serializers.CharField(source='zone.domain')

    class Meta:
        fields = ('id','data', 'target', 'ttl', 'domain')
        model = CanonicalNameRecord

    def create(self, validated_data):
        zone = Zone.objects.get(domain__name=validated_data['zone']['domain'])
        obj = CanonicalNameRecord(zone=zone,
                                  data=validated_data['data'],
                                  target=validated_data['target'],
                                  ttl=validated_data['ttl'])
        obj.save()
        return obj


class MailExchangeRecordSerializer(serializers.ModelSerializer):

    domain = serializers.CharField(source='zone.domain')

    class Meta:
        fields = ('id','data', 'priority', 'origin', 'ttl', 'domain')
        model = MailExchangeRecord

    def create(self, validated_data):
        zone = Zone.objects.get(domain__name=validated_data['zone']['domain'])
        obj = MailExchangeRecord(zone=zone,
                                 data=validated_data['data'],
                                 priority=validated_data['priority'],
                                 origin=validated_data['origin'],
                                 ttl=validated_data['ttl'])
        obj.save()
        return obj


class NameServerRecordSerializer(serializers.ModelSerializer):

    domain = serializers.CharField(source='zone.domain')

    class Meta:
        fields = ('id','data', 'origin', 'ttl', 'domain')
        model = NameServerRecord

    def create(self, validated_data):
        zone = Zone.objects.get(domain__name=validated_data['zone']['domain'])
        obj = NameServerRecord(zone=zone,
                               data=validated_data['data'],
                               origin=validated_data['origin'],
                               ttl=validated_data['ttl'])
        obj.save()
        return obj


class TextRecordSerializer(serializers.ModelSerializer):

    domain = serializers.CharField(source='zone.domain')

    class Meta:
        fields = ('id','data', 'text', 'ttl', 'domain')
        model = TextRecord

    def create(self, validated_data):
        zone = Zone.objects.get(domain__name=validated_data['zone']['domain'])
        obj = TextRecord(zone=zone,
                         data=validated_data['data'],
                         text=validated_data['text'],
                         ttl=validated_data['ttl'])
        obj.save()
        return obj


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