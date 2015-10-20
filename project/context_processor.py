from django.conf import settings


def app_name(request):
    name = getattr(settings, 'APP_NAME', 'Unknown')
    return {'APP_NAME': name}