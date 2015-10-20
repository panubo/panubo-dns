from django.conf import settings


def app_name(request):
    app_name = getattr(settings, 'APP_NAME', 'Unknown')
    return {'APP_NAME': app_name}