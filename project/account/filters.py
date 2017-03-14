

def filter_domain_queryset(qs, request):
    user = request.user
    if user.is_superuser:
        return qs
    return qs.filter(organisation_id__in=user.organisations.values_list('organisation_id', flat=True))


def filter_organisation_queryset(qs, request):
    user = request.user
    if user.is_superuser:
        return qs
    return qs.filter(pk__in=request.user.organisations.values_list('organisation_id', flat=True))


def filter_zone_queryset(qs, request):
    user = request.user
    if user.is_superuser:
        return qs
    return qs.filter(domain__organisation_id__in=user.organisations.values_list('organisation_id', flat=True))


# filter for addressrecordset etc on 'domain', 'data'
def filter_zonerecord_queryset(qs, request):
    user = request.user
    domain = request.query_params.get('domain', None)
    data = request.query_params.get('data', None)
    if domain is not None:
        qs = qs.filter(zone__domain__name=domain)
    if data is not None:
        qs = qs.filter(data=data)
    if user.is_superuser:
        return qs
    return qs.filter(zone__domain__organisation_id__in=user.organisations.values_list('organisation_id', flat=True))